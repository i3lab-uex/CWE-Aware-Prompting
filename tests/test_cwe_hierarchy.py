import json
from pathlib import Path
import zipfile

import pytest

from utils.cwe_hierarchy import (
    CWEDataError,
    CWEUnknownError,
    CWEUnsupportedAbstractionError,
    DEFAULT_XML_PATH,
    get_canonical_lineage,
    get_cwe_hierarchy,
    main,
)


NAMESPACE = "http://cwe.mitre.org/cwe-7"


def weakness(
    cwe_id: int,
    abstraction: str,
    parent: int | None = None,
    *,
    alternate_parent: int | None = None,
) -> str:
    relationships = ""
    if parent is not None or alternate_parent is not None:
        items = []
        if parent is not None:
            items.append(
                f'<Related_Weakness Nature="ChildOf" CWE_ID="{parent}" '
                'View_ID="1000" Ordinal="Primary"/>'
            )
        if alternate_parent is not None:
            items.append(
                f'<Related_Weakness Nature="ChildOf" CWE_ID="{alternate_parent}" '
                'View_ID="1000"/>'
            )
        relationships = f"<Related_Weaknesses>{''.join(items)}</Related_Weaknesses>"
    return (
        f'<Weakness ID="{cwe_id}" Name="Name {cwe_id}" '
        f'Abstraction="{abstraction}">'
        f"<Description> Description   for CWE-{cwe_id}. </Description>"
        f"{relationships}</Weakness>"
    )


@pytest.fixture
def xml_zip(tmp_path: Path) -> Path:
    entries = [
        weakness(1, "Pillar"),
        weakness(2, "Class", 1),
        weakness(3, "Base", 2),
        weakness(4, "Variant", 3, alternate_parent=6),
        weakness(5, "Base", 2),
        weakness(6, "Class", 1),
        weakness(7, "Variant", 6),
        weakness(8, "Base", 6),
        weakness(100, "Pillar"),
        weakness(101, "Base", 100),
        weakness(102, "Variant", 101),
        weakness(200, "Compound", 2),
    ]
    xml = (
        f'<Weakness_Catalog xmlns="{NAMESPACE}" '
        'Name="VIEW LIST: CWE-1000: Research Concepts" Version="test">'
        f"<Weaknesses>{''.join(entries)}</Weaknesses>"
        "</Weakness_Catalog>"
    )
    archive_path = tmp_path / "1000.xml.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("1000.xml", xml)
    return archive_path


def test_returns_complete_hierarchy_and_includes_input(xml_zip: Path) -> None:
    assert get_cwe_hierarchy(3, xml_path=xml_zip) == [
        {"cwe_id": 1, "distance": 2, "type": "Pillar"},
        {"cwe_id": 2, "distance": 1, "type": "Class"},
        {"cwe_id": 3, "distance": 0, "type": "Base"},
        {"cwe_id": 4, "distance": 1, "type": "Variant"},
    ]
    assert get_cwe_hierarchy("CWE-4", xml_path=xml_zip) == [
        {"cwe_id": 1, "distance": 3, "type": "Pillar"},
        {"cwe_id": 2, "distance": 2, "type": "Class"},
        {"cwe_id": 3, "distance": 1, "type": "Base"},
        {"cwe_id": 4, "distance": 0, "type": "Variant"},
    ]


def test_uses_nearest_fallback_inside_same_pillar(xml_zip: Path) -> None:
    assert get_cwe_hierarchy(5, xml_path=xml_zip) == [
        {"cwe_id": 1, "distance": 2, "type": "Pillar"},
        {"cwe_id": 2, "distance": 1, "type": "Class"},
        {"cwe_id": 5, "distance": 0, "type": "Base"},
        {"cwe_id": 4, "distance": 3, "type": "Variant"},
    ]


def test_omits_level_that_does_not_exist_in_pillar(xml_zip: Path) -> None:
    assert get_cwe_hierarchy(100, xml_path=xml_zip) == [
        {"cwe_id": 100, "distance": 0, "type": "Pillar"},
        {"cwe_id": 101, "distance": 1, "type": "Base"},
        {"cwe_id": 102, "distance": 2, "type": "Variant"},
    ]


def test_ignores_non_primary_parent(xml_zip: Path) -> None:
    assert [item["cwe_id"] for item in get_cwe_hierarchy(4, xml_path=xml_zip)] == [
        1,
        2,
        3,
        4,
    ]


def test_returns_normalised_official_descriptions(xml_zip: Path) -> None:
    assert get_cwe_hierarchy(
        "3", include_descriptions=True, xml_path=xml_zip
    ) == [
        {
            "cwe_id": 1,
            "distance": 2,
            "type": "Pillar",
            "description": "Description for CWE-1.",
        },
        {
            "cwe_id": 2,
            "distance": 1,
            "type": "Class",
            "description": "Description for CWE-2.",
        },
        {
            "cwe_id": 3,
            "distance": 0,
            "type": "Base",
            "description": "Description for CWE-3.",
        },
        {
            "cwe_id": 4,
            "distance": 1,
            "type": "Variant",
            "description": "Description for CWE-4.",
        },
    ]


@pytest.mark.parametrize("invalid_id", [0, -1, True, "", "CWE-x", "78x"])
def test_rejects_invalid_ids(xml_zip: Path, invalid_id: object) -> None:
    with pytest.raises(CWEUnknownError, match="inválido"):
        get_cwe_hierarchy(invalid_id, xml_path=xml_zip)  # type: ignore[arg-type]


def test_rejects_unknown_cwe(xml_zip: Path) -> None:
    with pytest.raises(CWEUnknownError, match="no pertenece"):
        get_cwe_hierarchy(999, xml_path=xml_zip)


def test_rejects_unsupported_abstraction(xml_zip: Path) -> None:
    with pytest.raises(CWEUnsupportedAbstractionError, match="Compound"):
        get_cwe_hierarchy(200, xml_path=xml_zip)


def test_canonical_lineage_supports_compound_without_sibling_fallback(
    xml_zip: Path,
) -> None:
    assert [
        (item["cwe_id"], item["abstraction"])
        for item in get_canonical_lineage(200, xml_path=xml_zip)
    ] == [(1, "Pillar"), (2, "Class"), (200, "Compound")]


def test_canonical_lineage_does_not_fill_levels_from_descendants_or_siblings(
    xml_zip: Path,
) -> None:
    assert [
        (item["cwe_id"], item["abstraction"])
        for item in get_canonical_lineage(1, xml_path=xml_zip)
    ] == [(1, "Pillar")]
    assert [
        (item["cwe_id"], item["abstraction"])
        for item in get_canonical_lineage(5, xml_path=xml_zip)
    ] == [(1, "Pillar"), (2, "Class"), (5, "Base")]


@pytest.mark.parametrize(
    ("cwe_id", "expected"),
    [
        (78, [(707, "Pillar"), (77, "Class"), (78, "Base")]),
        (95, [(707, "Pillar"), (74, "Class"), (94, "Base"), (95, "Variant")]),
        (352, [(693, "Pillar"), (345, "Class"), (352, "Compound")]),
    ],
)
def test_bundled_canonical_lineages(
    cwe_id: int, expected: list[tuple[int, str]]
) -> None:
    assert [
        (item["cwe_id"], item["abstraction"])
        for item in get_canonical_lineage(cwe_id)
    ] == expected


def test_rejects_wrong_view(tmp_path: Path) -> None:
    wrong_view = tmp_path / "wrong.xml"
    wrong_view.write_text(
        f'<Weakness_Catalog xmlns="{NAMESPACE}" Name="Other view"/>',
        encoding="utf-8",
    )
    with pytest.raises(CWEDataError, match="View 1000"):
        get_cwe_hierarchy(1, xml_path=wrong_view)


def test_rejects_corrupt_xml(tmp_path: Path) -> None:
    corrupt = tmp_path / "corrupt.xml"
    corrupt.write_text("<not-closed>", encoding="utf-8")
    with pytest.raises(CWEDataError, match="No se pudo leer"):
        get_cwe_hierarchy(1, xml_path=corrupt)


def test_cli_prints_json_with_descriptions(
    xml_zip: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["CWE-3", "--with-descriptions", "--xml", str(xml_zip)]) == 0
    captured = capsys.readouterr()
    assert [item["cwe_id"] for item in json.loads(captured.out)] == [1, 2, 3, 4]
    assert captured.err == ""


def test_cli_reports_unknown_cwe(
    xml_zip: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["999", "--xml", str(xml_zip)]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "error:" in captured.err


def test_bundled_mitre_archive_is_view_1000() -> None:
    assert DEFAULT_XML_PATH.is_file()
    result = get_cwe_hierarchy(552)
    assert result == [
        {"cwe_id": 664, "distance": 2, "type": "Pillar"},
        {"cwe_id": 668, "distance": 1, "type": "Class"},
        {"cwe_id": 552, "distance": 0, "type": "Base"},
        {"cwe_id": 219, "distance": 1, "type": "Variant"},
    ]
