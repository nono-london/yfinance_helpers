from setuptools import find_packages, setup

setup(
    name="yfinance_helpers",
    packages=find_packages(),
    version="0.0.0.1",
    description="Webcraps data from yahoo finance",
    author="Arnaud Dupuis",
    author_email="dupuis.a@outlook.com",
    license="Private",
    install_requires=["wheel", "yfinance", "pandas",
                      "psycopg2", "asyncpg", "lxml"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)

if __name__ == '__main__':
    pass
