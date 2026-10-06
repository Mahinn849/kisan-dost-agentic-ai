from pydantic import BaseModel, Field

class PestDiagnosis(BaseModel):
    status: str = Field(default="diagnosed", description="Diagnosis status (diagnosed, uncertain, unsupported_crop)")
    crop: str = Field(description="Crop investigated")
    symptoms_analyzed: str = Field(description="Symptoms reported by farmer")
    likely_problem: str = Field(description="Identified pest or pathological disease name")
    disease_type: str = Field(description="Category: Insect Pest, Fungal, Viral, Bacterial, or Physiological")
    severity: str = Field(description="Severity index: Low, Medium, High, or Critical")
    treatment: str = Field(description="Integrated pest management (IPM) and cultural practices")
    safe_chemical: str = Field(description="Government approved active chemical ingredient")
    safe_dosage: str = Field(description="Strict verified safe dosage per acre / per 100L water, or 'dosage_unavailable'")
    dosage_status: str = Field(description="Status of dosage: 'verified_safe' or 'dosage_unavailable'")
    safety_precautions: str = Field(description="Farmer safety, PPE, spray timing, and PHI (Pre-Harvest Interval)")
    source: str = Field(description="Data source: Agriculture Department Punjab or PlantVillage")
