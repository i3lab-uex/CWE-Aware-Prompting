"""Find a representative CWE hierarchy using MITRE Research View 1000."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Literal, overload, Sequence, TypedDict
import xml.etree.ElementTree as ET
import zipfile


VIEW_ID = "1000"
ABSTRACTION_ORDER = ("Pillar", "Class", "Base", "Variant")
CANONICAL_ABSTRACTION_ORDER = ("Pillar", "Class", "Base", "Variant", "Compound")
DEFAULT_XML_PATH = Path(__file__).parent.with_name("data") / "1000.xml.zip"


class CWEHierarchyError(ValueError):
    """Base error raised by CWE hierarchy operations."""


class CWEDataError(CWEHierarchyError):
    """Raised when the MITRE data file is missing or invalid."""


class CWEUnknownError(CWEHierarchyError):
    """Raised when a CWE is not present in Research View 1000."""


class CWEUnsupportedAbstractionError(CWEHierarchyError):
    """Raised when the input CWE is not Pillar, Class, Base, or Variant."""


class CWEResult(TypedDict):
    """Public representation of a selected CWE."""

    cwe_id: int
    distance: int
    type: str


class CWEWithDescription(CWEResult):
    """A selected CWE with its official description."""

    description: str


class CWECanonicalNode(TypedDict):
    """A node in the target's direct primary ``ChildOf`` lineage."""

    cwe_id: int
    name: str
    description: str
    abstraction: str
    distance: int


@dataclass(frozen=True)
class _CWERecord:
    cwe_id: int
    name: str
    abstraction: str
    description: str


@dataclass(frozen=True)
class _CWECatalog:
    records: dict[int, _CWERecord]
    primary_parent: dict[int, int]
    primary_children: dict[int, tuple[int, ...]]


def _normalise_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def _read_xml_root(path: Path) -> ET.Element:
    if not path.exists():
        raise CWEDataError(f"No existe el archivo de datos CWE: {path}")
    if not path.is_file():
        raise CWEDataError(f"La ruta de datos CWE no es un archivo: {path}")

    try:
        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                xml_files = [
                    name
                    for name in archive.namelist()
                    if name.lower().endswith(".xml") and not name.endswith("/")
                ]
                if len(xml_files) != 1:
                    raise CWEDataError(
                        "El ZIP de MITRE debe contener exactamente un archivo XML"
                    )
                with archive.open(xml_files[0]) as xml_file:
                    return ET.parse(xml_file).getroot()

        return ET.parse(path).getroot()
    except CWEDataError:
        raise
    except (ET.ParseError, OSError, zipfile.BadZipFile) as exc:
        raise CWEDataError(f"No se pudo leer el XML de MITRE: {path}") from exc


@lru_cache(maxsize=4)
def _load_catalog_cached(
    resolved_path: str, modified_ns: int, file_size: int
) -> _CWECatalog:
    del modified_ns, file_size
    root = _read_xml_root(Path(resolved_path))

    if "CWE-1000" not in root.attrib.get("Name", ""):
        raise CWEDataError("El XML no corresponde a la View 1000 de MITRE")

    if not root.tag.startswith("{"):
        raise CWEDataError("El XML de MITRE no contiene el namespace CWE esperado")
    namespace = root.tag.partition("}")[0] + "}"

    weaknesses = root.find(f"{namespace}Weaknesses")
    if weaknesses is None:
        raise CWEDataError("El XML de MITRE no contiene la sección Weaknesses")

    records: dict[int, _CWERecord] = {}
    weakness_elements: dict[int, ET.Element] = {}
    for weakness in weaknesses.findall(f"{namespace}Weakness"):
        raw_id = weakness.attrib.get("ID", "")
        try:
            cwe_id = int(raw_id)
        except ValueError as exc:
            raise CWEDataError(f"ID de CWE inválido en el XML: {raw_id!r}") from exc

        name = weakness.attrib.get("Name", "").strip()
        description = _normalise_text(weakness.find(f"{namespace}Description"))
        records[cwe_id] = _CWERecord(
            cwe_id=cwe_id,
            name=name,
            abstraction=weakness.attrib.get("Abstraction", ""),
            description=description or name,
        )
        weakness_elements[cwe_id] = weakness

    primary_parent: dict[int, int] = {}
    primary_children_lists: dict[int, list[int]] = defaultdict(list)
    relation_path = (
        f"{namespace}Related_Weaknesses/{namespace}Related_Weakness"
    )
    for child_id, weakness in weakness_elements.items():
        for relation in weakness.findall(relation_path):
            if not (
                relation.attrib.get("Nature") == "ChildOf"
                and relation.attrib.get("View_ID") == VIEW_ID
                and relation.attrib.get("Ordinal") == "Primary"
            ):
                continue

            try:
                parent_id = int(relation.attrib["CWE_ID"])
            except (KeyError, ValueError) as exc:
                raise CWEDataError(
                    f"Relación primaria inválida para CWE-{child_id}"
                ) from exc
            if parent_id not in records:
                raise CWEDataError(
                    f"CWE-{child_id} referencia al padre ausente CWE-{parent_id}"
                )
            if child_id in primary_parent:
                raise CWEDataError(
                    f"CWE-{child_id} tiene más de un padre primario en View 1000"
                )

            primary_parent[child_id] = parent_id
            primary_children_lists[parent_id].append(child_id)

    primary_children = {
        cwe_id: tuple(sorted(children))
        for cwe_id, children in primary_children_lists.items()
    }
    return _CWECatalog(records, primary_parent, primary_children)


def _load_catalog(xml_path: str | Path) -> _CWECatalog:
    path = Path(xml_path)
    try:
        stat = path.stat()
    except OSError as exc:
        raise CWEDataError(f"No existe el archivo de datos CWE: {path}") from exc
    return _load_catalog_cached(
        str(path.resolve()), stat.st_mtime_ns, stat.st_size
    )


def _parse_cwe_id(value: int | str) -> int:
    if isinstance(value, bool):
        raise CWEUnknownError(f"ID de CWE inválido: {value!r}")
    if isinstance(value, int):
        cwe_id = value
    elif isinstance(value, str):
        normalised = value.strip().upper()
        if normalised.startswith("CWE-"):
            normalised = normalised[4:]
        if not normalised.isdecimal():
            raise CWEUnknownError(f"ID de CWE inválido: {value!r}")
        cwe_id = int(normalised)
    else:
        raise CWEUnknownError(f"ID de CWE inválido: {value!r}")

    if cwe_id <= 0:
        raise CWEUnknownError(f"ID de CWE inválido: {value!r}")
    return cwe_id


def _ancestor_chain(catalog: _CWECatalog, cwe_id: int) -> list[int]:
    """Return the primary chain from its Pillar root to ``cwe_id``."""

    reverse_chain: list[int] = []
    visited: set[int] = set()
    current = cwe_id
    while True:
        if current in visited:
            raise CWEDataError("La jerarquía primaria de View 1000 contiene un ciclo")
        visited.add(current)
        reverse_chain.append(current)
        if current not in catalog.primary_parent:
            break
        current = catalog.primary_parent[current]

    chain = list(reversed(reverse_chain))
    if catalog.records[chain[0]].abstraction != "Pillar":
        raise CWEDataError(
            f"CWE-{cwe_id} no conduce a un Pillar mediante relaciones primarias"
        )
    return chain


def _descendant_paths(catalog: _CWECatalog, start: int) -> list[list[int]]:
    paths: list[list[int]] = []
    stack: list[tuple[int, list[int]]] = [(start, [start])]
    while stack:
        current, path = stack.pop()
        children = catalog.primary_children.get(current, ())
        if not children:
            paths.append(path)
            continue
        for child in reversed(children):
            if child in path:
                raise CWEDataError("La jerarquía primaria de View 1000 contiene un ciclo")
            stack.append((child, [*path, child]))
    return paths


def _best_path(catalog: _CWECatalog, cwe_id: int) -> list[int]:
    ancestors = _ancestor_chain(catalog, cwe_id)
    candidates = [
        [*ancestors[:-1], *descendants]
        for descendants in _descendant_paths(catalog, cwe_id)
    ]

    def ranking(
        path: list[int],
    ) -> tuple[int, int, int, tuple[int, ...], int, tuple[int, ...]]:
        input_position = path.index(cwe_id)
        representatives: list[int] = []
        representative_distances: list[int] = []
        for abstraction in ABSTRACTION_ORDER:
            candidates = [
                (abs(position - input_position), node_id)
                for position, node_id in enumerate(path)
                if catalog.records[node_id].abstraction == abstraction
            ]
            if not candidates:
                continue
            distance, representative = min(candidates)
            representatives.append(representative)
            representative_distances.append(distance)

        return (
            -len(representatives),
            sum(representative_distances),
            max(representative_distances, default=0),
            tuple(representatives),
            len(path),
            tuple(path),
        )

    return min(candidates, key=ranking)


def _distances_within_pillar(
    catalog: _CWECatalog, cwe_id: int, pillar_id: int
) -> dict[int, int]:
    pillar_nodes: set[int] = set()
    stack = [pillar_id]
    while stack:
        current = stack.pop()
        if current in pillar_nodes:
            continue
        pillar_nodes.add(current)
        stack.extend(catalog.primary_children.get(current, ()))

    distances = {cwe_id: 0}
    queue = deque([cwe_id])
    while queue:
        current = queue.popleft()
        neighbours = list(catalog.primary_children.get(current, ()))
        parent = catalog.primary_parent.get(current)
        if parent is not None:
            neighbours.append(parent)
        for neighbour in neighbours:
            if neighbour not in pillar_nodes or neighbour in distances:
                continue
            distances[neighbour] = distances[current] + 1
            queue.append(neighbour)
    return distances


def _select_cwes(
    catalog: _CWECatalog, cwe_id: int
) -> tuple[list[int], dict[int, int]]:
    record = catalog.records.get(cwe_id)
    if record is None:
        raise CWEUnknownError(f"CWE-{cwe_id} no pertenece a la View 1000")
    if record.abstraction not in ABSTRACTION_ORDER:
        raise CWEUnsupportedAbstractionError(
            f"CWE-{cwe_id} tiene abstracción no soportada: {record.abstraction or 'desconocida'}"
        )

    best_path = _best_path(catalog, cwe_id)
    input_position = best_path.index(cwe_id)
    selected: dict[str, int] = {record.abstraction: cwe_id}

    for abstraction in ABSTRACTION_ORDER:
        if abstraction in selected:
            continue
        candidates = [
            (abs(position - input_position), node_id)
            for position, node_id in enumerate(best_path)
            if catalog.records[node_id].abstraction == abstraction
        ]
        if candidates:
            selected[abstraction] = min(candidates)[1]

    pillar_id = best_path[0]
    distances = _distances_within_pillar(catalog, cwe_id, pillar_id)
    for abstraction in ABSTRACTION_ORDER:
        if abstraction in selected:
            continue
        fallback_candidates = [
            (distance, node_id)
            for node_id, distance in distances.items()
            if catalog.records[node_id].abstraction == abstraction
        ]
        if fallback_candidates:
            selected[abstraction] = min(fallback_candidates)[1]

    ordered = [
        selected[abstraction]
        for abstraction in ABSTRACTION_ORDER
        if abstraction in selected
    ]
    return ordered, distances


@overload
def get_cwe_hierarchy(
    cwe_id: int | str,
    include_descriptions: Literal[False] = False,
    xml_path: str | Path = DEFAULT_XML_PATH,
) -> list[CWEResult]: ...


@overload
def get_cwe_hierarchy(
    cwe_id: int | str,
    include_descriptions: Literal[True] = True,
    xml_path: str | Path = DEFAULT_XML_PATH,
) -> list[CWEWithDescription]: ...


def get_cwe_hierarchy(
    cwe_id: int | str,
    include_descriptions: bool = False,
    xml_path: str | Path = DEFAULT_XML_PATH,
) -> list[CWEResult] | list[CWEWithDescription]:
    """Return representative CWEs ordered as Pillar, Class, Base, Variant."""

    catalog = _load_catalog(xml_path)
    selected, distances = _select_cwes(catalog, _parse_cwe_id(cwe_id))
    results: list[CWEResult] = [
        {
            "cwe_id": selected_id,
            "distance": distances[selected_id],
            "type": catalog.records[selected_id].abstraction,
        }
        for selected_id in selected
    ]
    if not include_descriptions:
        return results
    return [
        {
            **result,
            "description": catalog.records[result["cwe_id"]].description,
        }
        for result in results
    ]


def get_canonical_lineage(
    cwe_id: int | str,
    xml_path: str | Path = DEFAULT_XML_PATH,
) -> list[CWECanonicalNode]:
    """Return the canonical primary lineage for a CWE target.

    Unlike :func:`get_cwe_hierarchy`, this experimental API never searches
    sibling branches to fill a missing abstraction.  It follows only primary
    ``ChildOf`` edges from the target to its Pillar, preserves the target, and
    collapses repeated abstraction levels by keeping the node nearest to the
    target.  ``Compound`` is supported here because CWE-352 is part of the
    experiment.  The legacy hierarchy API intentionally remains unchanged.
    """

    parsed_id = _parse_cwe_id(cwe_id)
    catalog = _load_catalog(xml_path)
    record = catalog.records.get(parsed_id)
    if record is None:
        raise CWEUnknownError(f"CWE-{parsed_id} no pertenece a la View 1000")
    if record.abstraction not in CANONICAL_ABSTRACTION_ORDER:
        raise CWEUnsupportedAbstractionError(
            f"CWE-{parsed_id} tiene abstracción no soportada: "
            f"{record.abstraction or 'desconocida'}"
        )

    # Walking outwards and using setdefault makes the target (distance zero),
    # or the closest ancestor at a repeated abstraction, authoritative.
    nearest: dict[str, tuple[int, int]] = {}
    current = parsed_id
    distance = 0
    visited: set[int] = set()
    while True:
        if current in visited:
            raise CWEDataError("La jerarquía primaria de View 1000 contiene un ciclo")
        visited.add(current)
        current_record = catalog.records[current]
        if current_record.abstraction not in CANONICAL_ABSTRACTION_ORDER:
            raise CWEUnsupportedAbstractionError(
                f"CWE-{current} tiene abstracción no soportada: "
                f"{current_record.abstraction or 'desconocida'}"
            )
        nearest.setdefault(current_record.abstraction, (current, distance))
        parent = catalog.primary_parent.get(current)
        if parent is None:
            break
        current = parent
        distance += 1

    root = catalog.records[current]
    if root.abstraction != "Pillar":
        raise CWEDataError(
            f"CWE-{parsed_id} no conduce a un Pillar mediante relaciones primarias"
        )

    result: list[CWECanonicalNode] = []
    for abstraction in CANONICAL_ABSTRACTION_ORDER:
        selected = nearest.get(abstraction)
        if selected is None:
            continue
        selected_id, selected_distance = selected
        selected_record = catalog.records[selected_id]
        result.append(
            {
                "cwe_id": selected_id,
                "name": selected_record.name,
                "description": selected_record.description,
                "abstraction": selected_record.abstraction,
                "distance": selected_distance,
            }
        )
    return result


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Obtiene una jerarquía Pillar/Class/Base/Variant de la View 1000 de MITRE."
        )
    )
    parser.add_argument("cwe_id", help="ID numérico o con formato CWE-<id>")
    parser.add_argument(
        "--with-descriptions",
        action="store_true",
        help="Incluye la descripción oficial de cada CWE",
    )
    parser.add_argument(
        "--xml",
        type=Path,
        default=DEFAULT_XML_PATH,
        help="Ruta al ZIP XML o XML sin comprimir de la View 1000",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = get_cwe_hierarchy(
            args.cwe_id,
            include_descriptions=args.with_descriptions,
            xml_path=args.xml,
        )
    except CWEHierarchyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
