import heapq
from datetime import datetime, timedelta
import json
import sys


if len(sys.argv) != 3:
    print "More arguments required, exit..."

input_file = sys.argv[1]
output_file = sys.argv[2]
latest_event = None

print "Input File Path: %s" % input_file
print "Output File Path: %s" % output_file


def check_valid(event):
    # Check created time
    if 'created_time' not in event:
        return False
    try:
        datetime.strptime(event['created_time'], "%Y-%m-%dT%H:%M:%SZ")
    except Exception as e:
        print e
        return False
    # Check target and actor
    if 'actor' not in event or 'target' not in event:
        return False
    return True


def check_time_window(events, new_event, g, e):
    global latest_event
    if len(events) == 0:
        latest_event = new_event[0]
        return True
    earliest_event = events[0]
    # if new event is older than earliest one
    if earliest_event[0] > new_event[0]:
        # Check 60s window
        if latest_event - timedelta(seconds=60) < new_event[0]:
            return True
        return False
    # if new event is within 60 seconds time window
    elif earliest_event[0] + timedelta(seconds=60) >= new_event[0]:
        return True
    # if new event is outside of 60 seconds time window, the earliest one will be removed
    else:
        event = heapq.heappop(events)
        update_graph_deletion(g, e, event)
        return check_time_window(events, new_event, g, e)


# Update Graph: Insert edge
def update_graph_insertion(g, e, event):
    edge = (event[1], event[2])
    edge_reverse = (event[2], event[1])
    if edge not in e:
        e.append(edge_reverse)
        e.append(edge)
    # Update degree
    if edge[0] not in g:
        g[edge[0]] = dict()
    if edge[1] not in g:
        g[edge[1]] = dict()
    g[edge[0]][edge[1]] = g[edge[0]].get(edge[1], 0) + 1
    g[edge[1]][edge[0]] = g[edge[1]].get(edge[0], 0) + 1


# Update Graph: Delete edge
def update_graph_deletion(g, e, event):
    edge = (event[1], event[2])
    edge_reverse = (event[2], event[1])
    g[edge[0]][edge[1]] = g[edge[0]].get(edge[1], 0) - 1
    g[edge[1]][edge[0]] = g[edge[1]].get(edge[0], 0) - 1
    if g[edge[0]][edge[1]] == 0:
        e.remove(edge)
        e.remove(edge_reverse)
        del g[edge[0]][edge[1]]
        del g[edge[1]][edge[0]]
        # remove node if it is disconnected in graph
        if len(g[edge[0]]) == 0:
            del g[edge[0]]
        if len(g[edge[1]]) == 0:
            del g[edge[1]]


# Generate edges list, empty values of 'actor' included
def generate_edges(events):
    edges = []
    for event in events:
        tuple_edge = (event[1], event[2])
        edges.append(tuple_edge)
    return edges


# Generate sorted degree sequence of the graph
def gen_sorted_degree_sequence(g):
    seq = []
    g_vertices = g.keys()
    for vertex in g_vertices:
        heapq.heappush(seq, len(g[vertex]))
    return [heapq.heappop(seq) for i in range(len(seq))]


# Calculate the median degree of the graph
def calc_median_degree(sq):
    n = len(sq)
    if n == 0:
        return 0.00
    elif n % 2:
        median_degree = sq[n/2]/1.00
    else:
        median_degree = (sq[n/2] + sq[n/2-1])/2.00
    return median_degree


trans_events = []
edges = []
graph = dict()
inputs = open(input_file)
outputs = file(output_file, "w")
for line in inputs:
    trans_event = json.loads(line)
    # validate event
    if check_valid(trans_event):
        timestamp = datetime.strptime(trans_event['created_time'], "%Y-%m-%dT%H:%M:%SZ")
        tuple_event = (timestamp, trans_event.get('target'),
                       trans_event.get('actor'))
        if check_time_window(trans_events, tuple_event, graph, edges):
            # TODO: Insert one payment and update graph
            heapq.heappush(trans_events, tuple_event)
            # Update latest event if necessary
            if tuple_event[0] > latest_event:
                latest_event = tuple_event[0]
            update_graph_insertion(graph, edges, tuple_event)
    # When a new event comes, we recalculate the median
    sorted_list = gen_sorted_degree_sequence(graph)
    result = calc_median_degree(sorted_list)
    print "Median Degree:", result
    # Write the output file
    outputs.write("{0:.2f}\n".format(result))













