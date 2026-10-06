# Moodle User Registration – Ant/Jenkins Assignment

## Project flow

`Users.xlsx` → `input/users.csv` → Python/Ant → `xml/users.xml`
→ XSD validation → XSLT → `sql/users.sql` → optional Ant SQL task

The uploaded workbook contained 15 records. Seven satisfy all requested validation rules.
`input/users.csv` is the original dataset; `input/users_valid.csv` is the manually cleaned
dataset used as the default input so the full build succeeds.

## Files

- `build.xml` – Ant pipeline.
- `scripts/csv_to_xml.py` – CSV-to-XML converter called by Ant.
- `xsd/users.xsd` – required-field and format validation.
- `xslt/users-to-sql.xsl` – XML-to-SQL transformation.
- `input/users.csv` – original spreadsheet data as CSV.
- `input/users_valid.csv` – cleaned CSV with offending records removed.
- `sql/create-staging-table.sql` – optional demo table.
- `sql/users.sql` – generated output after `ant transform`.

## Local Ant test

```bash
ant hello
ant
```

Expected first output:

```text
Hello World
```

The default build uses `input/users_valid.csv`, so it should produce:

- `xml/users.xml`
- `sql/users.sql`

### Prove that validation catches bad records

Run:

```bash
ant clean
ant -Dinput.csv=input/users.csv
```

This should fail during the `validate` target because the original spreadsheet contains
invalid records.

### Use another CSV

```bash
ant -Dinput.csv=input/users_valid.csv clean all
```

## Jenkins configuration

1. Install/configure Java and Ant on the Jenkins EC2 instance.
2. Install the Jenkins Git plugin and Ant tool/plugin as required by the course environment.
3. Create a Jenkins Freestyle project.
4. Under **Source Code Management → Git**, enter the GitHub repository URL.
5. Add the GitHub credentials/token if the repository is private.
6. Under **Build → Invoke Ant**, select the configured Ant installation and use:
   `clean all`
7. Save and **Build Now**.
8. Check the console output for:
   - `Hello World`
   - CSV-to-XML conversion
   - `XML validation passed.`
   - SQL generation

For a validation demonstration, configure the Ant target/input to use
`input/users.csv`; the Jenkins build should fail at `validate`.

## Optional database execution

The `sql` target uses Ant's SQL task and requires a JDBC driver. The JDBC JAR must be
available to Ant, typically in `$ANT_HOME/lib` or supplied with Ant's `-lib` option.

Example:

```bash
ant sql \
  -Ddb.driver=com.mysql.cj.jdbc.Driver \
  -Ddb.url="jdbc:mysql://DB_HOST:3306/moodle" \
  -Ddb.user="moodle" \
  -Ddb.password="REPLACE_ME"
```

Do not commit database passwords to GitHub.

## Important Moodle note

The generated SQL is deliberately aimed at `mdl_user_import` by default. Directly inserting
plain-text passwords into Moodle's core `mdl_user` table is not a safe/valid production
registration mechanism: Moodle expects its own password-hash format and has additional
user/account fields and application-level behavior.

For the assignment's SQL demonstration, use the supplied staging table or adapt the XSLT
after checking the exact Moodle version/schema and password-hashing requirements. In a real
Moodle deployment, prefer Moodle's supported web-service/CLI/application APIs for user
creation rather than bypassing them with raw SQL.

## Suggested Git commands

```bash
git init
git add .
git commit -m "Add Ant Moodle user registration pipeline"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```
