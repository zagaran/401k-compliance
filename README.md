# 401k-compliance

This code runs the 2019 ACP/ADP, Coverage, and Top-Heavy tests on a list of all your employee contributions to determine whether your organization as a whole is compliant with 401k non-discrimination laws.

Sources:
- ACP test: https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-the-plan-failed-the-401k-adp-and-acp-nondiscrimination-tests
- ADP test: https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-the-plan-failed-the-401k-adp-and-acp-nondiscrimination-tests
- Coverage test: https://www.law.cornell.edu/cfr/text/26/1.410(b)-2
- Top-Heavy test: https://www.irs.gov/irm/part4/irm_04-072-005#idm139991937781072


## Non-discrimination testing
Non-discrimination testing is required every year by the IRS for all (non-Safe Harbor) 401(k) plans in order to ensure that the plan is fair and accessible for all employees, regardless of their level of compensation or ownership interest. non-discrimination testing includes the ADP/ACP and Top Heavy non-discrimination tests.

Source for the following  content: https://my.guideline.com/sponsor/setup/faq

### The ADP/ACP non-discrimination tests
The Actual Deferral Percentage and Actual Contribution Percentage (ADP/ACP) tests are designed to ensure that a plan does not unfairly favor Highly Compensated Employees (HCEs). The ADP test assesses whether the plan is discriminating in favor of HCEs with respect to pre-tax and Roth employee deferrals, while the ACP test looks at employer matching contributions.

Testing is intended to accomplish two primary goals:

1. Prevent 401(k)s from becoming a tax haven for HCEs. Because contributing to a 401(k) comes with significant tax advantages, a plan could fall into the trap of being almost exclusively enjoyed by company owners and executives.
2. Ensure that Non-Highly Compensated Employees (NHCEs) have a fair opportunity to take part in plan benefits.
If testing determines that a plan is unfairly discriminating in favor of HCEs, the plan will need to make corrections by refunding excess contributions to HCEs, making employer contributions to NHCEs, or using a combination of both methods.

### The Top-Heavy test
Top-heavy testing is designed to ensure key employees are not being unfairly favored in the 401(k) plan design. A plan is considered “top-heavy” if the total value of the accounts of Key Employees exceeds 60% of the total value of all plan assets.

### Definitions

- HCE vs. NHCE
Non-discrimination testing uses two main employee classifications for the purposes of its calculations: Highly Compensated Employees and Non-Highly Compensated Employees.

    - A Highly Compensated Employee (HCE) is an individual who:
        - Owns greater than 5% of the company at any time during the plan year or preceding year; OR
        - Received compensation from the company of more than $120,000 (for 2016 and 2017) for the preceding year AND (if the employer chooses*) was in the top 20% of employees when ranked by compensation.
    *Note: This code utilizes the top 20% election for small employers as it generally benefits the business for testing purposes.

    - A Non-Highly Compensated Employee (NHCE) is any employee that does not fall into the HCE category.

- Key Employee
    The top-heavy test uses Key Employees in calculations.

    - A Key Employee is:
        - An officer making over $170,000 (2016) or $175,000 (2017); OR
        - Someone who owns more than 5% of the business; OR
        - An employee owning more than 1% of the business AND making over $150,000 for the plan year.
    - A non-key employee is an employee who does not fall under the Key employee category.
