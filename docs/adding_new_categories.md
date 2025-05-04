# How to Add New Evaluation Categories to NEAR Rubric MCP

This guide will help you add new evaluation categories to your NEAR Rubric MCP project using the `create_category.py` helper script. No deep technical knowledge is required—just follow the steps below!

---

## What is a Category?

A **category** is a specific area your project is evaluated on (for example: "NEAR Integration", "Code Quality", "Team Activity"). Each category has its own score and criteria.

If you want to evaluate projects on new aspects (like "Security" or "User Experience"), you can add a new category.

---

## Step 1: Open a Terminal

- On Windows, you can use PowerShell.
- Make sure you are in the `near-rubric-mcp` directory.

---

## Step 2: Run the Category Creation Script

Use the following command, replacing the example values with your own:

```bash
python scripts/create_category.py --name "Your Category Name" --points 10 --indicators "First thing to look for" "Second thing" --file-patterns "**/*.rs" "**/*.js" --high-criteria "What a perfect score looks like" --medium-criteria "What a medium score looks like" --low-criteria "What a low score looks like"
```

**Example:**  
To add a category called "Security" worth 10 points:

```bash
python scripts/create_category.py --name "Security" --points 10 --indicators "Use of audits" "No critical vulnerabilities" --file-patterns "**/*.rs" "**/*.js" --high-criteria "No vulnerabilities, audited" --medium-criteria "Minor issues, not audited" --low-criteria "Major vulnerabilities"
```

**Tip:**  
You can add up to 4 indicators and 3 file patterns. If you add fewer, the script will fill in the rest for you.

---

## Step 3: What Happens Next?

The script will:
- Create a new category file in `near-rubric-mcp/categories/`
- Create a prompt template in `near-rubric-mcp/resources/prompts/`
- Update the main rubric configuration in `near-rubric-mcp/config/rubric.yaml`
- Update file pattern configuration in `near-rubric-mcp/config/patterns.yaml`

You'll see a summary in your terminal.

---

## Step 4: Validate and Review

1. **Validate your changes:**  
   Run:
   ```bash
   python scripts/validate_config.py
   ```
   This checks for errors in your configuration.

2. **Review the generated files:**  
   - Category logic: `near-rubric-mcp/categories/your_category_name.py`
   - Prompt template: `near-rubric-mcp/resources/prompts/your_category_name.txt`
   - Config updates: `near-rubric-mcp/config/rubric.yaml` and `patterns.yaml`

---

## Step 5: Next Steps

- If validation passes, your new category is ready to use!
- If you see errors, check the messages in your terminal and review the files above.

---

## Troubleshooting

- **Script not found?** Make sure you are in the `near-rubric-mcp` directory and use the correct path: `python scripts/create_category.py`
- **Permission errors?** Try running your terminal as administrator.
- **Need help?** Contact the maintainers or check the README for more info.

---

## More Information

- See [docs/near_rubric.md](near_rubric.md) for examples of existing categories and scoring guidelines.
- For advanced options, run:
  ```bash
  python scripts/create_category.py --help
  ```

---

**Ready to add your own categories? Give it a try!** 