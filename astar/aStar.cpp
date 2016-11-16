#include <bits/stdc++.h>
#include "aStar.h"
#define all(c) c.begin(), c.end()
#define tr(container, it) for(auto it = container.begin(); it != container.end(); it++)
#define present(c,x) ((c).find(x) != (c).end())
#define cpresent(c,x) (find(all(c),x) != (c).end())
#define mp make_pair
#define fi first
#define se second
AStar::AStar() : goal( "12345678B" ) {
}

AStar4::AStar4() {
	goal = "1238B4765";
}

void AStar::input() {
	string begin = "";
	string end = "";
	string tmp;
	getline(cin,tmp);
	for(int x = 0;x < 3;x++){
		for(int y = 0;y < 3;y++){
			string tile;
			cin>>tile;
			if(tile.size()>1) {
				begin += tile[1];
			} else {
				begin += tile[0];
			}
		}
	}
	cin>>tmp;cin>>tmp;
	for(int x = 0;x < 3;x++){
		for(int y = 0;y < 3;y++){
			string tile;
			cin>>tile;
			if(tile.size()>1) {
				end += tile[1];
			} else {
				end += tile[0];
			}
		}
	}
	start = begin;
	goal = end;
}

int AStar::heuristicCost(string n,string g) {
	return 0;
}

void AStar::reconstructPath( map<string,string>& cameFrom, string current ) {
	int cost = 0;
	while( true ) {
		decodeState( current );
		cout<<"  ^\n";
		cout<<"  |";
		cost++;
		current = cameFrom[current];
		if( current == "" ) {
			break;
		}
	}
	cout<<"\nOptimal Cost: "<<cost<<"\n";
}

void AStar::decodeState( string state ) {
	for( int x = 0;x < state.size();x++ ) {
		char c = state[x];
		if( x % 3 == 0 ) {
			cout<<"\n";
		}
		cout<<c<<" ";
	}
	cout<<"\n";
}

void AStar::aStar() {
	bool success = false;
	long statesExp = 0;
	set<is> fScore;
	set<string> closedSet,openSet;
	map<string,int> gScore;

	gScore.insert( mp( start, 0 ) );

	map<string,string> cameFrom;	
	cameFrom.insert( mp( start, "" ) );

	fScore.insert( mp( heuristicCost( start, goal ), start ) );
	openSet.insert( start );
	
	while( fScore.size() > 0 ) {
		statesExp++;
		auto current = *fScore.begin();
		if( current.second == goal ) {
			success = true;
			cout<<"Success!\n";
			cout<<"Start state:";
			decodeState( start );
			cout<<"Goal state:";
			decodeState( goal );
			cout<<"Optimal Path:\n";
			reconstructPath( cameFrom, current.second );
			cout<<"Total states explored:"<<statesExp<<"\n";
			cout<<"Open List:\n";
			tr( openSet, it ) {
				decodeState( *it );
			}
			cout<<"Close List:\n";
			tr( closedSet, it ) {
				decodeState( *it );
			}
		}
		fScore.erase( current );
		openSet.erase( current.second );
		closedSet.insert( current.second );
		// get neighbours
		int B = 0;
		for( int x = 0;x < 10;x++ ) {
			if( current.second[x] == 'B' ) {
				B = x;
				break;
			}
		}
		for( int x = 0;x < 4;x++ ) {
			if( nextN[B][x] == -1 ) {
				break;
			}
			string temp = current.second;

			char tmp = temp[ nextN[B][x] ];
			temp[nextN[B][x]] = 'B';
			temp[B] = tmp;

			// check if temp in closedSet
			if( closedSet.find( temp ) != closedSet.end() )
				continue;
			int tentative_gs = gScore.find( current.second )->second + 1;
			
			if( openSet.find( temp ) == openSet.end() ) {
				openSet.insert( temp );
			} else if( tentative_gs >= gScore.find( temp )->second ) {
				continue;
			}

			cameFrom[temp] = current.second;
			gScore[temp] = tentative_gs;
			fScore.insert( mp( gScore[temp] + heuristicCost( temp, goal ), temp ) );
		
		}
	}
	if( !success ) {
		cout<<"Failure!\n";
		cout<<"Start state:";
		decodeState( start );
		cout<<"Goal state:";
		decodeState( goal );
	}
}

int AStar2::heuristicCost( string n, string goal ) {
	int hn = 0;
	for( int x = 0;x < n.size();x++ ) {
		char c = n[x];
		if( x + 1 != c - '0' )
			hn++;
	}
	return hn;
}

int AStar3::heuristicCost( string n, string goal ) {
	int hn = 0;
	for( int x = 0;x < n.size();x++ ) {
		int c = n[x] - '0';
		hn += manhattan[x][c];
	}
	return hn;
}

int AStar4::heuristicCost( string n, string goal ) {
	int hn = 0;
	for( int x = 0;x < n.size();x++ ) {
		int c = n[x] - '0';
		hn += manhattan[x][c];
		if( x!= 5 ) {
			int suc = succ[x];
			if( n[suc] - '0' != ( c + 1 ) % 8 )
				hn += 2;
		}

	}
	return hn + 1;
}
