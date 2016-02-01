#Facebook Member Tree creator

Creates a "family" tree for a Facebook group where members invite other members.

This assumes the original creator still exists, but might not get it completely right.   

Orphan trees are those where ancestors have left FB or the group.   As there is no easy way of figuring out who the parents are (without asking someone), each just has their own tree.  Also, because of the last point, the actual owner might be orphaned.

To create this:
- Check out this code (you can use git, or just download the zip)
- Go to group members page
- Scroll to bottom and click "See More" until there are no more pages
- Open up your browser console and copy in the code from get_members.js (or firefox_get_members.js if you are using firefox). And run it.  You MUST have popups enabled for this to work.   
- Save the results as members.json (This is the default, you can call it whatever you want) in the same directory as the code is located
- Run: python tree.py \[ -f \<filename\> \] (you only use -f if you didn't save the file as members.json)
