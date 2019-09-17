from lxml import html
import math


def get_value_by_attr(attr, tree):
    base = "//b[contains(text(), '%s')]/../following-sibling::td" % attr
    if attr in ["Indirizzo web", "Posta elettronica", "Commercio elettronico"]:
        base += "/a"

    value = ''

    try:
        value = tree.xpath("%s/text()" % base)[0].strip()
    except IndexError as e:
        print("[ERROR] %s" % str(e))

    return value


def create_json(attrs, tree):
    my_contact = {}
    for attr in attrs:
        my_contact[attr] = get_value_by_attr(attr, tree)
    return my_contact


def get_contact_by_crawled_page(pageText, fields):
    tree = html.fromstring(pageText)
    contact = create_json(fields, tree)
    return contact


def count_from_search(tree):
    tot_results = int(tree.xpath(
        '//html/body/center/table[2]/tr[2]/td[1]/table[1]/tr/td/table[2]/tr/td[1]/font/text()[2]')[0].lstrip(
        ' \xa0 n° '))
    tot_pages = math.ceil(tot_results / 10)
    return tot_results, tot_pages


def get_result_pages(tree):
    pages = []

    for i in range(3, 13):
        xpath = "/html/body/center/table[2]/tr[2]/td[1]/table[1]/tr/td/table[%d]/tr[2]/td/table/tr/td[2]/a[" \
                "1]/@onclick" % i

        try:
            pages.append("ricerca/%s" % tree.xpath(xpath)[0][14:-33])
        except IndexError as e:
            print("ERR: %s" % str(e))

    return pages
