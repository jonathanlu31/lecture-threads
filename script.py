import argparse
from datetime import datetime

from edapi import EdAPI

from config import TEST_COURSE_ID, COURSE_ID, HOLIDAYS

# Post template
TEMPLATE = """<document version="2.0">
<paragraph>Please ask any questions you have about lecture {lec_no} below!</paragraph>
</document>
"""

def main(course_id):
    holiday_dates = [datetime.strptime(date_str, '%m/%d/%y').date() for date_str in HOLIDAYS]

    if datetime.today().date() in holiday_dates:
        return

    ed = EdAPI()
    ed.login()

    with open("lec_num.txt", 'r+', encoding='utf-8') as f:
        lec_no = f.read()
        f.seek(0)
        f.write(str(int(lec_no) + 1))

    ed.post_thread(course_id, params={
        "type": "post",
        "title": f"Lecture {lec_no}",
        "category": "Lectures",
        "content": TEMPLATE.format(lec_no=lec_no),
        "is_pinned": True,
        "is_anonymous": False,
        "is_megathread": True,
        "anonymous_comments": True
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="perform actions on test Ed")
    args = parser.parse_args()
    course_id = (TEST_COURSE_ID if args.test else COURSE_ID)

    main(course_id)
