from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from process_data.predictive_analysis.ProductsRecommendationAnalysis import ProductsRecommendationAnalysis
from utils.utils import GLOBAL_DFS

predictive_router = APIRouter(prefix="/predictive", tags=["Predictive Analysis"])


class RecommendRequest(BaseModel):
    name_product: str = Field(..., description="Tên sản phẩm.")
    topk: int = Field(..., description="Top k của sản phẩm.")


@predictive_router.post("/recommend", summary="Gợi ý sản phẩm.")
def recommend(request: RecommendRequest):
    try:
        result = ProductsRecommendationAnalysis().recommend(
            GLOBAL_DFS["Product_Recommendation.csv"],
            name_column="name",
            sim_column="sim",
            name_product=request.name_product,
            topk=request.topk
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
