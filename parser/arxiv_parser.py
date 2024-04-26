import urllib
import feedparser

# класс для парсинга статей
class Parser:
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query?"
        self.start = 0
        self.max_results = 5

    def __call__(self, search_query, max_results=None):
        """
        поиск первых статей по запросу
        возвращает list(dict), где dict - отдельная статья

        :search_query: - str, запрос
        :max_results: - int, органичение сверху на количество статей
        """
        search = "all:" + urllib.parse.quote_plus(search_query)
        if max_results is None:
            max_results = self.max_results

        query = "search_query=%s&start=%i&max_results=%i" % (
            search,
            self.start,
            max_results,
        )
        response = urllib.request.urlopen(self.base_url + query).read()
        feed = feedparser.parse(response)

        articles = []
        for entry in feed.entries:
            authors = ", ".join(author.name for author in entry.authors)
            abs_link, pdf_link = None, None
            for link in entry.links:
                if link.rel == "alternate":
                    abs_link = link.href
                elif link.title == "pdf":
                    pdf_link = link.href
            article = self.create_article(
                id=entry.id.split("/abs/")[-1],
                date=entry.published,
                title=entry.title,
                authors=authors,
                abs_link=abs_link,
                pdf_link=pdf_link,
                summary=entry.summary,
            )
            articles.append(article)

        return articles

    def create_article(self, id, date, title, authors, abs_link, pdf_link, summary):
        """
        создает словарь, описывающий статью с ключами:

        :id: - str, id на arxiv.org
        :date: - str, дата публикации
        :title: - str, название
        :authors: - str, авторы
        :abs_link: - str, ссылка на страницу статьи
        :pdf_link: - str, ссылка на pdf
        :summary: - str, краткое содержание
        """
        book = {}
        book["id"] = id
        book["date"] = date
        book["title"] = title
        book["authors"] = authors
        book["abs_link"] = abs_link
        book["pdf_link"] = pdf_link
        book["summary"] = summary

        return book
