import GrapherH
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Input the path(as string) to the csv")
args = parser.parse_args()
GrapherH.GrapherH().produceGraph(args.path)