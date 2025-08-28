import glob
import json
import os
import subprocess
from tests.test_cases import TESTS, MAX_SCORE

REPORT_DIR = 'tests/reports'
os.makedirs(REPORT_DIR, exist_ok=True)

submissions = sorted(glob.glob('./submissions/*.py'))
# print("Found submissions:", submissions)

rows = []

for sub in submissions:
    student_id = os.path.basename(sub).replace('.py', '').lower()
    if not student_id.startswith('s'):
        # print(f"Skipping non-student file: {sub}")
        continue
    print(f"Grading submission: {student_id}")
    report = {
        'student_id': student_id,
        'submission': sub,
        'tests': [],
        'total_score': 0,
        'max_score': MAX_SCORE
    }

    for idx, t in enumerate(TESTS):
        try:
            completed = subprocess.run(
                ['python', './tests/exec_test.py', '--submission', sub, '--test-index', str(idx)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=8,
                text=True
            )
        except subprocess.TimeoutExpired:
            out = json.dumps({
                'passed': False,
                'error_reason': 'TimeoutExceeded',
                'output': None,
                'time_ms': None,
                'exception': 'Timeout'
            })
            res = json.loads(out)
            res['test_name'] = t['name']
            res['points'] = t['points']
        else:
            if completed.returncode != 0 and completed.stdout.strip() == '':
                # Something crashed hard — include stderr
                res = {
                    'passed': False,
                    'error_reason': 'Execution failed',
                    'output': None,
                    'time_ms': None,
                    'exception': completed.stderr,
                    'test_name': t['name'],
                    'points': t['points']
                }
            else:
                try:
                    res = json.loads(completed.stdout)
                except Exception as e:
                    res = {
                        'passed': False,
                        'error_reason': 'Malformed runner output',
                        'output': completed.stdout,
                        'time_ms': None,
                        'exception': completed.stderr,
                        'test_name': t['name'],
                        'points': t['points']
                    }

        # scoring
        if res.get('passed'):
            report['total_score'] += t['points']
        else:
            # attach human readable failure reason
            if res.get('error_reason') is None:
                res['error_reason'] = 'Unknown failure'

        report['tests'].append(res)

    # write report
    report_path = os.path.join(REPORT_DIR, f'{student_id}.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    passed = sum(1 for x in report['tests'] if x.get('passed'))
    failed = len(report['tests']) - passed

    rows.append({
        'student_id': student_id,
        'total_score': report['total_score'],
        'max_score': report['max_score'],
        'passed_tests': passed,
        'failed_tests': failed,
        'report_path': report_path
    })

# write CSV
import csv

with open('tests/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['student_id', 'total_score', 'max_score', 'passed_tests', 'failed_tests', 'report_path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print('Grading finished. Results saved to results.csv and reports/ per student.')
