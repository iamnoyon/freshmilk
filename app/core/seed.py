from app.core.db import sessionLocal
from app.modules.user.model import User
from app.utils.hash_password import password_hash
from app.utils.permissions import Permission


def seed_superadmin():
    db = sessionLocal()
    existing = db.query(User).filter(User.phone == "0000000000").first()
    if not existing:
        superadmin = User(
            name="Super Admin",
            nid="0000000000",
            phone="01889010237",
            password=password_hash("1234"),
            role="superadmin",
            area="mirpurdosh",
            road="0",
            house="0",
            flat="0",
            permissions=[p.value for p in Permission],
        )
        db.add(superadmin)
        db.commit()
    db.close()
