from typing import List, Optional, Tuple
from collections import defaultdict
import warnings

from mp_api.core.client import BaseRester

from mp_api.routes.grain_boundary.models import GBTypeEnum, GrainBoundaryDoc


class GrainBoundaryRester(BaseRester):

    suffix = "grain_boundary"
    document_model = GrainBoundaryDoc  # type: ignore
    primary_key = "task_id"

    def search_grain_boundary_docs(
        self,
        material_ids: Optional[List[str]] = None,
        gb_energy: Optional[Tuple[float, float]] = None,
        separation_energy: Optional[Tuple[float, float]] = None,
        rotation_angle: Optional[Tuple[float, float]] = None,
        sigma: Optional[int] = None,
        type: Optional[GBTypeEnum] = None,
        chemsys: Optional[str] = None,
        num_chunks: Optional[int] = None,
        chunk_size: int = 1000,
        all_fields: bool = True,
        fields: Optional[List[str]] = None,
    ):
        """
        Query grain boundary docs using a variety of search criteria.

        Arguments:
            task_ids (List[str]): List of Materials Project IDs to query with.
            gb_energy (Tuple[float,float]): Minimum and maximum grain boundary energy in J/m³ to consider.
            separation_energy (Tuple[float,float]): Minimum and maximum work of separation energy in J/m³ to consider.
            rotation_angle (Tuple[float,float]): Minimum and maximum rotation angle in degrees to consider.
            sigma (int): Sigma value of grain boundary.
            type (GBTypeEnum): Grain boundary type.
            chemsys (str): Dash-delimited string of elements in the material.
            num_chunks (int): Maximum number of chunks of data to yield. None will yield all possible.
            chunk_size (int): Number of data entries per chunk.
            all_fields (bool): Whether to return all fields in the document. Defaults to True.
            fields (List[str]): List of fields in GrainBoundaryDoc to return data for.
                Default is material_id and last_updated if all_fields is False.

       Returns:
            ([GrainBoundaryDoc]) List of grain boundary documents
        """

        query_params = defaultdict(dict)  # type: dict

        if material_ids:
            query_params.update({"task_ids": ",".join(material_ids)})

        if gb_energy:
            query_params.update({"gb_energy_min": gb_energy[0], "gb_energy_max": gb_energy[1]})

        if separation_energy:
            query_params.update({"w_sep_energy_min": separation_energy[0], "w_sep_energy_max": separation_energy[1]})

        if rotation_angle:
            query_params.update({"rotation_angle_min": rotation_angle[0], "rotation_angle_max": rotation_angle[1]})

        if sigma:
            query_params.update({"sigma": sigma})

        if type:
            query_params.update({"type": type})

        if chemsys:
            query_params.update({"chemsys": chemsys})

        query_params = {entry: query_params[entry] for entry in query_params if query_params[entry] is not None}

        return super().search(
            version=self.version,
            num_chunks=num_chunks,
            chunk_size=chunk_size,
            all_fields=all_fields,
            fields=fields,
            **query_params
        )
