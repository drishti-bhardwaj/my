from django.urls import path

from . import views
from . import advanced_views


urlpatterns = [

    # =====================================================
    # HEALTH CHECK
    # Used by Render to verify the service is alive.
    # =====================================================

    path(
        "health/",
        views.health_check,
        name="health_check",
    ),


    # =====================================================
    # 1. CONTROL CENTER
    # =====================================================

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),


    # =====================================================
    # 2. MATERIAL INTELLIGENCE
    # DOCUMENT INGESTION / OCR / EXTRACTION
    # =====================================================

    path(
        "extract/",
        views.document_ingest,
        name="document_ingest",
    ),

    path(
        "ingest/",
        views.document_ingest,
    ),

    path(
        "materials/ingest/",
        views.document_ingest,
    ),


    # =====================================================
    # 3. MATERIAL COMPARATOR
    # =====================================================

    path(
        "comparator/",
        views.compare_materials_view,
        name="comparator",
    ),

    path(
        "comparator/feedback/",
        views.record_comparator_feedback,
        name="record_comparator_feedback",
    ),


    # =====================================================
    # 4. DIGITAL COMPLIANCE TWIN
    # =====================================================

    path(
        "compliance/",
        advanced_views.compliance_view,
        name="compliance",
    ),


    # =====================================================
    # 5. FINANCIAL SAVINGS + CARBON
    # =====================================================

    path(
        "savings/",
        advanced_views.savings_view,
        name="savings",
    ),


    # =====================================================
    # 6. PROCUREMENT INTELLIGENCE
    # =====================================================

    path(
        "procurement/",
        advanced_views.procurement_view,
        name="procurement",
    ),


    # =====================================================
    # 7. CAD / 3D MATCHER
    # =====================================================

    path(
        "cad/",
        advanced_views.cad_view,
        name="cad_matcher",
    ),


    # =====================================================
    # 8. MULTILINGUAL INGESTION
    # =====================================================

    path(
        "multilingual/",
        advanced_views.multilingual_view,
        name="multilingual",
    ),


    # =====================================================
    # 9. DATA LINEAGE
    # =====================================================

    path(
        "lineage/",
        advanced_views.lineage_view,
        name="data_lineage",
    ),


    # =====================================================
    # 10. AUDIT + GOVERNANCE
    # =====================================================

    path(
        "audit/",
        views.audit_trail,
        name="audit_trail",
    ),


    # =====================================================
    # 11. CANDIDATE GROUPS
    # =====================================================

    path(
        "groups/<int:group_id>/",
        views.group_detail,
        name="group_detail",
    ),


    # =====================================================
    # 12. NATIONAL MATERIAL MASTER
    # =====================================================

    path(
        "national-master/",
        views.national_master,
        name="national_master",
    ),

    path(
        "national-master/<int:material_id>/",
        views.national_material_detail,
        name="national_material_detail",
    ),

    path(
        "national-master/<int:material_id>/review/",
        views.review_national_material,
        name="review_national_material",
    ),


    # =====================================================
    # 13. SOURCE CATALOGUE
    # =====================================================

    path(
        "catalogue/",
        views.source_catalogue,
        name="source_catalogue",
    ),

    path(
        "catalogue/<int:material_id>/",
        views.material_detail,
        name="material_detail",
    ),


    # =====================================================
    # 14. ADVANCED INTELLIGENCE HUB
    # =====================================================

    path(
        "advanced/",
        advanced_views.advanced_center,
        name="advanced_center",
    ),


    # =====================================================
    # 15. ERP DUPLICATE DETECTOR API
    # =====================================================

    path(
        "api/erp-duplicate-check/",
        advanced_views.erp_duplicate_api,
        name="erp_duplicate_api",
    ),

    path(
        "api/confidence-breakdown/",
        views.confidence_breakdown_api,
        name="confidence_breakdown_api",
    ),

    path(
        "api/savings-simulation/",
        views.savings_simulation_api,
        name="savings_simulation_api",
    ),

]