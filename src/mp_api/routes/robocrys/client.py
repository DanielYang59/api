from mp_api.core.client import BaseRester
from mp_api.routes.robocrys.models import RobocrysDoc


class RobocrysRester(BaseRester):

    suffix = "robocrys"
    document_model = RobocrysDoc  # type: ignore

    def search_robocrys_text(self, keywords: list[str]):
        """
        Search text generated from Robocrystallographer.

        Arguments:
            keywords (List[str]): List of search keywords

        Returns:
            robocrys_docs (List[RobocrysDoc]): List of robocrystallographer documents
        """

        keyword_string = ",".join(keywords)

        results = self._query_resource(
            criteria={"keywords": keyword_string},
            suburl="text_search",
            use_document_model=True,
        )

        return results
