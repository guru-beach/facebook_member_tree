import re
import copy
import json
from datetime import datetime
from operator import itemgetter, attrgetter
from optparse import OptionParser
# Need to explicitly set utf-8 or suffer
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

parser = OptionParser()
parser.add_option('-c', '--indent_char', dest="indent_char", default=" ", help="Character used to indent.  Default is ' '.")
parser.add_option('-f', '--file', dest="infile", default="members.json", help="JSON file to load.  Default is members.json.")
parser.add_option('-n', '--indent_width', dest="indent_width", type='int', default=4, help="How wide the indent is between levels.  Default=4")
parser.add_option('-o', '--orphan_multiple', dest="orphan_multiple", type='int', default=3, help="How many level numbers to highlight orphans.  Default=3")
(options, args) = parser.parse_args()
# The character to use when indenting, typically space, but can be anything
# like "+" or "," for CSV
indent_char = options.indent_char
# How many indents characters to write between levels
indent_width = options.indent_width
# When displaying ancestry depth, multiple by this.
# e.g.
# orphan_multiple = 3
# 111 Foo
#    222 Woo
orphan_multiple = options.orphan_multiple

infile = options.infile

members = {}
orphans = []
dead_orphans = []
most_prolific = [0]
date_format = "%A, %B %d, %Y at %I:%M%p"

def get_parent(parent_line):
  """Transforms parent string to just the name.   If no parent, returns None, typically this is the person who started the group or an orphan"""
  # Capturing the or'd strings because they don't seem to work on their own
  add_re = re.compile("(Invited|Added) by (.*?) (on|over|about|\d+|last) .*")
  try:
    parent = add_re.match(parent_line).group(2)
  except: 
    # This is probably an orphan
    parent = None
  return parent


def get_datetime(date, date_format=date_format):
  return datetime.strptime(date, date_format)

  
def gen_tree(member):
  global most_prolific
  try:
    ancestors = members[member]['ancestors']
    depth = len(ancestors)
  except:
    depth = 0
  if depth > 0:
    parent = ancestors[-1]
  else:
    parent = "None: The Boss!"
  # Start at 1
  depth_text = str(depth + 1)
  if boss not in ancestors and member != boss:
    depth_text *= orphan_multiple
  descendent_count = members[member]['descendents']
  children = members[member]['children']
  child_count = len(children)
  if child_count == most_prolific[0]:
    most_prolific.append(member)
  if child_count >most_prolific[0]:
    most_prolific = [child_count, member]
  status = ''
  if member in dead_orphans:
    status = 'DEAD'

  #print "{} {} {} -- Parent: {}, Child Count: {}, Descendent Count {}, Record {}".format(indent_char * indent_width * depth, depth_text, member, parent, child_count, descendent_count, members[member]) 
  print "{} {} {} - Descendents: {} {}".format(indent_char * indent_width * depth, depth_text, member, descendent_count, status) 

  for child in children:
    try: 
      gen_tree(child)
    except:
      pass

def count_descendents(member, ancestors):
  # Skip root
  # print "{} {}".format(member, ancestors)
  if len(ancestors) > 0:
    for ancestor in ancestors:
     members[ancestor]['descendents'] += 1
  # Need a copy or the next modification will modify the list!
  members[member]['ancestors'] = copy.copy(ancestors)
  # Push onto the stack
  ancestors.append(member)
  children = members[member]['children']
  # Prevent circular logic by removing children that are ancestors
  for child in children:
    if child in ancestors:
      children.remove(child)
  for child in children:
    count_descendents(child, ancestors)
  # Pop off from the stack
  ancestors.pop()

def init_member(name):
  members[name] = { 'children' : [],
                    'ancestors' : [],
                    'descendents' : 0,
                    'parent' : None
                  }

def main():
  global boss
  global orphans
  global dead_orphans
  with open(infile, 'r') as IN:
    members_json = json.load(IN)
    for name in members_json.keys():
      timestamp = get_datetime(members_json[name]['timestamp'])
      try:
        # parent is a javascript reserved word, so used adder
        parent_line = members_json[name]['adder']
        # Transform parent to just a name
        parent = get_parent(parent_line)
      except:
        # If there is no adder, this is the primary record
        boss = name
        parent = None
      # Add the member record if it's not there
      if not name in members:
        init_member(name)
      # Add the parent record if it's not there
      if not parent in members and parent:
        init_member(parent)
      if parent:
        members[parent]['children'].append(name)
      members[name]['parent'] = parent

  
  #print members
  count_descendents(boss, [])

  # Finds orphans and will create trees for them
  for member in members.keys():
    # The boss won't be an orphan
    if member == boss:
      pass
    #print "{} : {}".format(members[member], members[member]['ancestors'])
    # Parent will be None for boss and orphans
    elif members[member]['parent'] == None:
      orphans.append(member)
      count_descendents(member, [])
    if member not in members_json:
      dead_orphans.append(member)
  
  roots = [boss]
  # Double check for "real" orphans, not just order orphans
  for orphan in orphans:
    if not members[orphan]['parent']:
      roots.append(orphan)
  total_members = 0
  for root in roots:
    total_members += members[root]['descendents'] + 1
    gen_tree(root)
  print "Total members:         {}".format(len(members_json))
  print "Total members counted: {}".format(total_members)
  print "Dead orphan count:     {}".format(len(dead_orphans))
  print "Dead orphans:          {}".format(','.join(dead_orphans))
  print "Most Prolific:         {} with {} children".format(','.join(most_prolific[1:]), most_prolific[0])


if __name__ == '__main__':
  main()
