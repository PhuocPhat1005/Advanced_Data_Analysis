from typing import List, Literal

from fastapi import APIRouter, Query, HTTPException

from backend import dataset
from process_data.descriptive_analysis.DisplayStatusAnalysis import DisplayStatusAnalysis
from process_data.descriptive_analysis.QuantityAnalysis import QuantityAnalysis
from process_data.descriptive_analysis.RatingAnalysis import RatingAnalysis
from process_data.descriptive_analysis.RevenueStatusAnalysis import RevenueStatusAnalysis

descriptive_router = APIRouter(prefix="/descriptive", tags=["Descriptive Analysis"])


@descriptive_router.get("/revenue/timeline", summary="Get revenue by timeline.")
def get_revenue_by_timeline(
        categorized_column: str = Query(..., description="Tên cột phân loại."),
        time_mode: str = Query("D", regex="^[DMY]$", description="Chế độ thời gian: D=ngày, M=tháng, Y=năm.")
):
    try:
        result = RevenueStatusAnalysis().getRevenueByTimeline(
            dataset.product_revenue_df,
            "revenue",
            categorized_column,
            "date_created",
            time_mode
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@descriptive_router.get("/revenue/total", summary="Get total revenue.")
def get_total_revenue(
        categorized_column: str = Query(..., description="Tên cột phân loại."),
        min_date: str = Query(default="2016-01-01", description="Mốc thời gian tối thiểu YYYY-MM-DD, VD: 2016-01-01."),
        max_date: str = Query(..., description="Mốc thời gian tối đa YYYY-MM-DD, VD: 2020-01-03.")
):
    try:
        result = RevenueStatusAnalysis().getTotalRevenue(
            dataset.product_revenue_df,
            "revenue",
            categorized_column,
            "date_created",
            min_date,
            max_date
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@descriptive_router.get("/products/quantity/grouped", summary="Get product quantity grouped by factors.")
def get_quantity_by_group(
        factor_group_columns: List[str] = Query(..., description="Các cột phân nhóm (VD: category, region)."),
        min_date: str = Query("2016-01-01", description="Ngày bắt đầu (YYYY-MM-DD), VD: 2016-01-01."),
        max_date: str = Query(..., description="Ngày kết thúc (YYYY-MM-DD), VD: 2020-01-03.")
):
    try:
        result = QuantityAnalysis().getQuantityOfProductsByFactorGroup(
            dataset.product_quantity_df,
            "quantity_sold",
            factor_group_columns,
            "date_created",
            min_date,
            max_date
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@descriptive_router.get("/ratings/reviews/count/by-factor", summary="Get review count grouped by factor.")
def get_review_count_by_factor(
        factor_column: str = Query(..., description="Cột để phân nhóm."),
        by_function: Literal["sum", "mean"] = Query("sum", description="Hàm tổng hợp.")
):
    try:
        result = RatingAnalysis().getReviewCountByFactor(
            dataset.product_rating_df,
            "review_count",
            factor_column,
            by_function
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@descriptive_router.get("/ratings/average/by-factors", summary="Get average rating by factors.")
def get_avg_rating_by_factors(
        factor_columns: List[str] = Query(..., description="Các cột để phân nhóm.")
):
    try:
        result = RatingAnalysis().getAvgRatingByFactors(
            dataset.product_rating_df,
            "rating_average",
            factor_columns
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@descriptive_router.get("/status/display/by-factor", summary="Get display status count by factor.")
def get_display_status_by_factor(
        factor_column: str = Query(..., description="Cột phân nhóm."),
        min_date: str = Query("2016-01-01", description="Ngày bắt đầu lọc (YYYY-MM-DD), VD: 2016-01-01."),
        max_date: str = Query(..., description="Ngày kết thúc lọc (YYYY-MM-DD), VD: 2020-01-03.")
):
    try:
        result = DisplayStatusAnalysis().getDisplayStatusByFactor(
            dataset.product_display_status_df,
            "status",
            factor_column,
            "date_created",
            min_date,
            max_date
        )
        return {"total": len(result), "records": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
