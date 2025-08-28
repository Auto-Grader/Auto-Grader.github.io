import argparse
import json
import importlib.util
import sys
import time
import traceback
from tests.test_cases import TESTS


def load_and_run(submission_path, test_input, timeout_sec=5):
    """
    Load the student's module from path and call `bubble_sort` on a copy of test_input.
    Returns a dict with fields: passed(bool), error_reason(str|None), output(value), time_ms, exception
    """
    start = time.time()
    try:
        spec = importlib.util.spec_from_file_location('student_module', submission_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        return {
            'passed': False,
            'error_reason': 'ImportError: ' + repr(e),
            'output': None,
            'time_ms': int((time.time() - start) * 1000),
            'exception': traceback.format_exc()
        }

    if not hasattr(mod, 'bubble_sort'):
        return {
            'passed': False,
            'error_reason': 'No function bubble_sort(arr) found in submission',
            'output': None,
            'time_ms': int((time.time() - start) * 1000),
            'exception': None
        }

    func = getattr(mod, 'bubble_sort')

    import copy
    arr = copy.deepcopy(test_input)

    try:
        t0 = time.time()
        result = func(arr)
        t1 = time.time()
        time_ms = int((t1 - t0) * 1000)
    except Exception as e:
        return {
            'passed': False,
            'error_reason': 'RuntimeError: ' + repr(e),
            'output': None,
            'time_ms': int((time.time() - start) * 1000),
            'exception': traceback.format_exc()
        }

    # Determine final array
    final = None
    if result is None:
        final = arr
    else:
        final = result

    return {
        'passed': final == test_input_sorted(test_input),
        'error_reason': None if final == test_input_sorted(
            test_input) else f'Output mismatch. Got={final}, Expected={test_input_sorted(test_input)}',
        'output': final,
        'time_ms': time_ms,
        'exception': None
    }


def test_input_sorted(x):
    # For tests where expected is None (mixed types), we can't call sorted(); handled elsewhere.
    try:
        return sorted(x)
    except Exception:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--submission', required=True)
    parser.add_argument('--test-index', type=int, required=True)
    args = parser.parse_args()

    test = TESTS[args.test_index]
    test_input = test['input']

    result = load_and_run(args.submission, test_input)
    # For test where expected is None (mixed types), we consider test passed if exception raised
    if test['expected'] is None:
        if result.get('exception'):
            result['passed'] = True
            result['error_reason'] = None
        else:
            # If no exception raised, but sorting produced something, mark as failed
            result['passed'] = False
            result[
                'error_reason'] = 'Expected TypeError or similar for mixed types, but function returned successfully.'

    # Add metadata
    result['test_name'] = test['name']
    result['points'] = test['points']

    print(json.dumps(result))
