# raw_list pandoc filter

This gives the ability to mix the numbering in lists, by splitting every listitem in one dedicated list.

### usage:
##### command:
```bash
pandoc example.md -o example.pdf --filter=./raw_lists.py
```
##### in md file:
```markdown
```{#list-1 .raw_list}
2. example text
3. third item
1. test text
\``` <-- you have to remove the backslash (escaping ´ in codeblocks is weird)
```