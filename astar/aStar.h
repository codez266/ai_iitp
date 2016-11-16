// AStar.h for A* class
#ifndef AStar_H
#define AStar_H
#include <bits/stdc++.h>
using namespace std;
typedef pair<int,string> is;
class AStar {
	protected:
		string start, goal;
	int nextN [9][4]={{1,3,-1,-1},{0,2,4,-1},{1,5,-1,-1},{0,4,6,-1},{1,3,5,7},{2,4,8,-1},{3,7,-1,-1},{8,6,4,-1},{5,7,-1,-1}};
	short manhattan[9][9] = {
					{0,1,2,1,2,3,2,3,4},
					{1,0,1,2,1,2,3,2,3},
					{2,1,0,3,2,1,4,3,2},
					{1,2,3,0,1,2,1,2,3},
					{2,1,2,1,0,1,2,1,2},
					{3,2,1,2,1,0,3,2,1},
					{2,3,4,1,2,3,0,1,2},
					{3,2,3,2,1,2,1,0,1},
					{4,3,2,3,2,1,2,1,0}};
	short succ[9] = {1, 2, 5, 0, -1, 8, 3, 6, 7};
	public:
		AStar();
		void input();
		virtual int heuristicCost( string n, string goal );
		void reconstructPath( map<string,string>& cameFrom, string current );
		void decodeState( string state );
		void aStar();	
};
class AStar2 : public AStar {
	int heuristicCost( string n, string goal );
};
class AStar3 : public AStar {
	int heuristicCost( string n, string goal );
};
class AStar4 : public AStar {
	public:
		int heuristicCost( string n, string goal );
		AStar4();
};
#endif
