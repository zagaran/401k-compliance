class Employee(object):
    name = None
    percentage_min = None
    percentage_max = None
    is_5_percent_owner = False
    is_key_employee = False
    key_employee_reason = None
    w2 = None

    def __init__(self, name, w2):
        self.name = name
        self.w2 = w2

    def __repr__(self):
        if self.percentage_min == self.percentage_max:
            percentage = f'{self.percentage_min}%'
        else:
            percentage = f'{self.percentage_min}% - {self.percentage_max}%'
        return f'<{self.name}: ${self.w2} at {percentage}>'

    @property
    def percentage_avg(self):
        return (self.percentage_min + self.percentage_max) / 2

    def set_amount(self, amount_min, amount_max=None):
        self.percentage_max = round(100 * (amount_max or amount_min) / self.w2)
        self.percentage_min = round(100 * amount_min / self.w2)
        return self

    def set_as_5_percent_owner(self):
        self.is_5_percent_owner = True
        self.key_employee_reason = KeyEmployeeReasons.is_5_percent_owner
        self.is_key_employee = True
        return self

    def set_as_key_employee(self, reason=None):
        if reason == KeyEmployeeReasons.is_5_percent_owner:
            self.set_as_5_percent_owner()
        else:
            self.key_employee_reason = reason
            self.is_key_employee = True
        return self

    def set_percentage(self, percentage_min, percentage_max=None):
        self.percentage_max = percentage_max or percentage_min
        self.percentage_min = percentage_min
        return self


class KeyEmployeeReasons(object):
    is_5_percent_owner = '5% owner'
    is_1_percent_owner = '1% owner and W2 > $150,000'


EMPLOYEES = [
    Employee('Person 1', 50000).set_amount(19000),
    Employee('Person 2', 50000).set_amount(10000, 19000),
    Employee('Person 3', 50000).set_percentage(5),
    Employee('Person 4', 50000).set_percentage(1, 10),
    Employee('Person 5', 50000).set_percentage(5).set_as_key_employee(reason=KeyEmployeeReasons.is_5_percent_owner),
    Employee('Person 6', 50000).set_percentage(50).set_as_5_percent_owner(),
]


def run_401k_tests(employees, conservative=True, top_paid_group_election=True):
    """
    Run all 401(k) tests.
    """
    hce_list, nhce_list = _get_hce_and_nhce(
        employees,
        top_paid_group_election=top_paid_group_election,
    )

    print(acp_test(hce_list, nhce_list, conservative=conservative))
    print(adp_test(hce_list, nhce_list, conservative=conservative))
    print(coverage_test(hce_list, nhce_list, conservative=conservative))
    print(top_heavy_test(employees, conservative=conservative))



def acp_test(hce_list, nhce_list, conservative=True):
    """
    Run the ACP test on employees.

    Note: This is assuming current year testing.

    Source: https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-the-plan-failed-the-401k-adp-and-acp-nondiscrimination-tests
    """
    if conservative:
        hce_average = (
            sum([hce.percentage_max for hce in hce_list]) / len(hce_list)
        )
        nhce_average = (
            sum([nhce.percentage_min for nhce in nhce_list]) / len(nhce_list)
        )
    else:
        hce_average = (
            sum([hce.percentage_avg for hce in hce_list]) / len(hce_list)
        )
        nhce_average = (
            sum([nhce.percentage_avg for nhce in nhce_list]) / len(nhce_list)
        )

    if nhce_average <= 2:
        hce_average_max = nhce_average * 2
    elif 2 < nhce_average <= 8:
        hce_average_max = nhce_average + 2
    else:
        hce_average_max = nhce_average * 1.25

    if hce_average <= hce_average_max:
        passed = True
    else:
        passed = False
    return (
        f'ADP test {"passed" if passed else "failed"}. NHCE average: {nhce_average:.2f}%, '
        f'HCE average: {hce_average:.2f}%, Max passing HCE average: {hce_average_max:.2f}%.'
    )



def adp_test(hce_list, nhce_list, conservative=True):
    """
    Run the ADP test on employees.

    Note: This is assuming no match, so this test is the same as the acp test.

    Source: https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-the-plan-failed-the-401k-adp-and-acp-nondiscrimination-tests
    """
    acp_test_result = acp_test(
        hce_list,
        nhce_list,
        conservative=conservative,
    )
    return acp_test_result.replace('ACP', 'ADP')



def coverage_test(hce_list, nhce_list, conservative=True):
    """
    Run the coverage test on employees.

    Note: This is assuming we calculate based on 1.410(b)(1)(b).

    Source: https://www.law.cornell.edu/cfr/text/26/1.410(b)-2
    """
    if conservative:
        hce_benefit_percentage = (
            len([hce for hce in hce_list if hce.percentage_max > 0]) / len(hce_list)
        )
        nhce_benefit_percentage = (
            len([nhce for nhce in nhce_list if nhce.percentage_min > 0]) / len(nhce_list)
        )
    else:
        hce_benefit_percentage = (
            len([hce for hce in hce_list if hce.percentage_avg > 0]) / len(hce_list)
        )
        nhce_benefit_percentage = (
            len([nhce for nhce in nhce_list if nhce.percentage_avg > 0]) / len(nhce_list)
        )

    participation_ratio = nhce_benefit_percentage / hce_benefit_percentage

    if participation_ratio >= 0.7:
        passed = True
    else:
        passed = False
    return (
        f'Coverage test {"passed" if passed else "failed"}. NHCE to HCE participation ratio is '
        f'{participation_ratio:.2%} (must be >= 70%).'
    )


def top_heavy_test(employees, conservative=True):
    """
    Run the top-heavy test on employees.

    Note: This currently only tests the contribution plan and not the benefits plan (if there is
          no match or profit sharing, the benefits plan should equal the contribution plan).

    Source: https://www.irs.gov/irm/part4/irm_04-072-005#idm139991937781072
    """
    key_employees_list = [employee for employee in employees if employee.is_key_employee]
    non_key_employees_list = [employee for employee in employees if not employee.is_key_employee]
    if conservative:
        key_employees_assets = sum([ke.w2 * ke.percentage_max for ke in key_employees_list])
        non_key_employees_assets = sum(
            [nke.w2 * nke.percentage_min for nke in non_key_employees_list]
        )
    else:
        key_employees_assets = sum([ke.w2 * ke.percentage_avg for ke in key_employees_list])
        non_key_employees_assets = sum(
            [nke.w2 * nke.percentage_avg for nke in non_key_employees_list]
        )

    top_percentage = key_employees_assets / (key_employees_assets + non_key_employees_assets)
    if top_percentage > 0.6:
        passed = False
    else:
        passed = True
    return (
        f'Top-heavy test {"passed" if passed else "failed"}. Key employees own '
        f'{top_percentage:.2%} of assets in the plan for this year.'
    )


def _get_hce_and_nhce(employees, hce_w2=125000, top_paid_group_election=True):
    """
    Calculate who is classified as HCE or NHCE.

    Note: If top_paid_group_election is True, we do not have a rule set up to break ties in W2
          salary. (1.414(q)-1T(A-3)(b))  Also, it's unclear from my research exactly how this
          election works: according to the IRS website, an employee is considered HCE if they
          "received compensation... of more than $120,000..., and, if the employer so chooses, was
          in the top 20% of employees when ranked by compensation"; however, the only way that
          this election makes sense is if you can only choose one method, not both (otherwise,
          it would never make sense not to take the election. This method assumes the latter.

    Sources:
      - https://www.irs.gov/retirement-plans/plan-participant-employee/definitions
      - https://www.law.cornell.edu/cfr/text/26/1.414(q)-1T
      - https://www.irs.gov/pub/irs-tege/epche603.pdf (page 32+)

    """
    if top_paid_group_election:
        sorted_employees = sorted(employees, key=lambda employee: employee.w2, reverse=True)
        number_of_hce = round(len(employees) * 0.2)
        hce_list = []
        nhce_list = []
        for employee in employees:
            if employee.is_5_percent_owner or employee in sorted_employees[:number_of_hce]:
                hce_list.append(employee)
            else:
                nhce_list.append(employee)
    else:
        hce_list = [employee for employee in employees if employee.w2 >= hce_w2]
        nhce_list = [employee for employee in employees if employee.w2 < hce_w2]

    return hce_list, nhce_list
