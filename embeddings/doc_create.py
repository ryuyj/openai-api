# imports
import mwclient  # for downloading example Wikipedia articles
import mwparserfromhell  # for splitting Wikipedia articles into sections
import openai  # for generating embeddings
import os  # for environment variables
import pandas as pd  # for DataFrames to store article sections and embeddings
import re  # for cutting <ref> links out of Wikipedia articles
import tiktoken  # for counting tokens

# get Wikipedia pages about the 2022 Winter Olympics

CATEGORY_TITLE = "Category:2002 FIFA World Cup"
WIKI_SITE = "en.wikipedia.org"


def titles_from_category(
    category: mwclient.listing.Category, max_depth: int
) -> set[str]:
    """주어진 위키 카테고리와 그 하위 카테고리의 페이지 제목 집합을 반환합니다."""
    titles = set()
    for cm in category.members():
        if type(cm) == mwclient.page.Page:
            # ^type() used instead of isinstance() to catch match w/ no inheritance
            titles.add(cm.name)
        elif isinstance(cm, mwclient.listing.Category) and max_depth > 0:
            deeper_titles = titles_from_category(cm, max_depth=max_depth - 1)
            titles.update(deeper_titles)
    return titles


site = mwclient.Site(WIKI_SITE)
category_page = site.pages[CATEGORY_TITLE]
titles = titles_from_category(category_page, max_depth=1)
# ^note: max_depth=1 means we go one level deep in the category tree
print(f"Found {len(titles)} article titles in {CATEGORY_TITLE}.")

# define functions to split Wikipedia pages into sections

SECTIONS_TO_IGNORE = [
    "See also",
    "References",
    "External links",
    "Further reading",
    "Footnotes",
    "Bibliography",
    "Sources",
    "Citations",
    "Literature",
    "Footnotes",
    "Notes and references",
    "Photo gallery",
    "Works cited",
    "Photos",
    "Gallery",
    "Notes",
    "References and sources",
    "References and notes",
]


def all_subsections_from_section(
    section: mwparserfromhell.wikicode.Wikicode,
    parent_titles: list[str],
    sections_to_ignore: set[str],
) -> list[tuple[list[str], str]]:
    """
    위키백과 섹션에서 중첩된 모든 하위 섹션의 평면화된 목록을 반환합니다.
    각 하위 섹션은 튜플입니다:
        - 첫 번째 요소는 페이지 제목으로 시작하는 상위 하위 섹션의 목록입니다.
        - 두 번째 요소는 하위 섹션의 텍스트입니다(자식은 포함되지 않음).
    """
    headings = [str(h) for h in section.filter_headings()]
    title = headings[0]
    if title.strip("=" + " ") in sections_to_ignore:
        # ^wiki headings are wrapped like "== Heading =="
        return []
    titles = parent_titles + [title]
    full_text = str(section)
    section_text = full_text.split(title)[1]
    if len(headings) == 1:
        return [(titles, section_text)]
    else:
        first_subtitle = headings[1]
        section_text = section_text.split(first_subtitle)[0]
        results = [(titles, section_text)]
        for subsection in section.get_sections(levels=[len(titles) + 1]):
            results.extend(all_subsections_from_section(subsection, titles, sections_to_ignore))
        return results


def all_subsections_from_title(
    title: str,
    sections_to_ignore: set[str] = SECTIONS_TO_IGNORE,
    site_name: str = WIKI_SITE,
) -> list[tuple[list[str], str]]:
    """위키백과 페이지 제목에서 중첩된 모든 하위 섹션의 평면화된 목록을 반환합니다.
    각 하위 섹션은 튜플입니다:
        - 첫 번째 요소는 페이지 제목으로 시작하는 상위 하위 섹션의 목록입니다.
        - 두 번째 요소는 하위 섹션의 텍스트입니다(자식은 포함되지 않음).
    """
    site = mwclient.Site(site_name)
    page = site.pages[title]
    text = page.text()
    parsed_text = mwparserfromhell.parse(text)
    headings = [str(h) for h in parsed_text.filter_headings()]
    if headings:
        summary_text = str(parsed_text).split(headings[0])[0]
    else:
        summary_text = str(parsed_text)
    results = [([title], summary_text)]
    for subsection in parsed_text.get_sections(levels=[2]):
        results.extend(all_subsections_from_section(subsection, [title], sections_to_ignore))
    return results

# split pages into sections
# may take ~1 minute per 100 articles
wikipedia_sections = []
for title in titles:
    wikipedia_sections.extend(all_subsections_from_title(title))
print(f"Found {len(wikipedia_sections)} sections in {len(titles)} pages.")

