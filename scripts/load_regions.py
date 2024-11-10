import json
from pathlib import Path

from core.models import Region, District

BASE_DIR = Path(__file__).resolve().parent.parent


def run():
    districts_json = open(BASE_DIR / "districts.json", "r+")
    districts_list = json.loads(districts_json.read())
    for obj in districts_list:
        if Region.objects.filter(name=obj['region'].strip()).exists():
            count = 1
            region = Region.objects.get(name=obj['region'].strip())
            for each in obj.get('districts', []):
                if District.objects.filter(name=each.strip(),region=region).exists():
                    District.objects.filter(name=each.strip(),region=region).update(code=f"{region.code}{count}")
                    count += 1
                else:
                    district = District(name=each.strip())
                    district.region = region
                    district.code = f"{region.code}{count}"
                    district.save()
                    count += 1
        else:
            region = Region(name=obj['region'].strip(), code=obj['code'].strip())
            region.save()
            region.refresh_from_db()
            count = 1
            for each in obj.get('districts', []):
                if District.objects.filter(name=each.strip(),region=region).exists():
                    District.objects.filter(name=each.strip(),region=region).update(code=f"{region.code}{count}")
                    count += 1
                else:
                    district = District(name=each.strip())
                    district.region = region
                    district.code = f"{region.code}{count}"
                    district.save()
                    count += 1

            if region.code is None:
                region.code = obj['code'].strip()
                region.save()
            count = 1
            for each in obj.get('districts', []):
                if District.objects.filter(name=each.strip(),region=region).exists():
                    District.objects.filter(name=each.strip(),region=region).update(code=f"{region.code}{count}")
                    count += 1
                else:
                    district = District(name=each.strip())
                    district.region = region
                    district.code = f"{region.code}{count}"
                    district.save()
                    count += 1
