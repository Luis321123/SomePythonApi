from sqlalchemy.orm import Session

from app.core.settings import get_settings

from app.models import BusinessUnit
from app.models import Discipline
from app.models import DocumentType
from app.models import ManagementArea
from app.seeders import disciplines
from app.seeders import document_type
from app.seeders import business_unit
from app.seeders import managements_areas


settings = get_settings()

def init_db(db: Session) -> None:
# Create all business_unit in BD for data.json

    data_business_unit = business_unit.data
    for item_document_unit in data_business_unit:
        business_units = db.query(BusinessUnit).where(BusinessUnit.name == item_document_unit['name']).first()
        if not business_units:
            business_units = BusinessUnit(
                name=item_document_unit['name'],
                acronym=item_document_unit['acronym'],
                active=item_document_unit['active']
            )
            db.add(business_units)
            db.commit()
            db.refresh(business_units)



# Create all document_type in BD for data.json
    data_document_type = document_type.data  
    for item_document_type in data_document_type:
        document_types = db.query(DocumentType).where(DocumentType.name == item_document_type['name']).first()
        if not document_types:
            document_types = DocumentType(
                name=item_document_type['name'],
                acronym=item_document_type['acronym'],
                active=item_document_type['active']
          
            )
            db.add(document_types)
            db.commit()
            db.refresh(document_types)


# Create all disciplines in BD for data.json
    data_disciplines = disciplines.data  
    for item_discipline in data_disciplines:
        discipline = db.query(Discipline).where(Discipline.name == item_discipline['name']).first()
        if not discipline:
            discipline = Discipline(
                name=item_discipline['name'],
                acronym=item_discipline['acronym'],
                active=item_discipline['active']
            )
            db.add(discipline)
            db.commit()
            db.refresh(discipline)
    
# Create all management_areas in BD for data.json
    data_management_area = managements_areas.data  
    for item_management in data_management_area:
        management_area = db.query(ManagementArea).where(ManagementArea.name == item_management['name']).first()
        if not management_area:
            management_area = ManagementArea(
                name=item_management['name'],
                acronym=item_management['acronym'],
                active=item_management['active']
            )
            db.add(management_area)
            db.commit()
            db.refresh(management_area)