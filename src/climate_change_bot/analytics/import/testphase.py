import re

pattern = r"\d+\.(\d+)\.\d+"


def add_testphase(df):
    print("Add testphase")
    testphase = []
    for row in df.to_dict('records'):
        match = re.match(pattern, row['chatbot_version'])
        if match:
            testphase.append(int(match.group(1)))
        else:
            raise ImportError(f"Could not extract testphase from version {row['chatbot_version']}")

    df['testphase'] = testphase
