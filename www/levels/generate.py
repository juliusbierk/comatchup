import numpy as np 
import json
import random
import Queue
from copy import deepcopy

levels_per_season = 25

for N in range(3,8+1):
	print N
	dots = N
	blocks_list = [N-1,N,N+1]

	season = N-2
	iterations = 150


	level = 1
	while level<=levels_per_season:
		blocks = random.choice(blocks_list)
		arr = list()
		for _ in range(N):
			arr.append([0]*N)

		########################
		def do_move(move, a):
			dx, dy = move
			new = deepcopy(a)
			# Do move
			for x in range(max([-dx, 0]), min([N, N-dx])):
				for y in range(max([-dy, 0]), min([N, N-dy])):
					if a[x][y]==1 or a[x][y]==6:
						new[x+dx][y+dy] += 1
						new[x][y] -= 1
			# Move back if on block
			for x in range(max([-dx, 0]), min([N, N-dx])):
				for y in range(max([-dy, 0]), min([N, N-dy])):
					if new[x+dx][y+dy] == -1:
						new[x+dx][y+dy] -= 1
						new[x][y] += 1
			# Move back if two in same spot
			valid = False
			while not valid:
				valid = True
				for x in range(max([-dx, 0]), min([N, N-dx])):
					for y in range(max([-dy, 0]), min([N, N-dy])):
						if new[x+dx][y+dy] == 2 or new[x+dx][y+dy] == 7:
							new[x+dx][y+dy] -= 1
							new[x][y] += 1
							valid = False
							break
					if not valid:
						break

			# On goals:
			on_goal = 0
			for x in range(N):
				for y in range(N):
					if new[x][y] == 6:
						on_goal += 1
			return new, dots==on_goal
		####################################
		moves = [(1,0),(-1,0),(0,1),(0,-1)]

		############## MAKE RANDOM LEVEL ##################
		def randint():
			return random.randint(0,N-1)

		### Insers 1 for dots
		for _ in range(dots):
			i = randint()
			j = randint()
			while arr[i][j] != 0:
				i = randint()
				j = randint()
			arr[i][j] += 1

		### Insers -2 for blocks
		for _ in range(blocks):
			i = randint()
			j = randint()
			while arr[i][j] != 0:
				i = randint()
				j = randint()
			arr[i][j] = -2

		# Move dots randomly
		original = deepcopy(arr)
		for _ in xrange(iterations):
			move = moves[random.randint(0,3)]
			arr,_ = do_move(move, arr)
		for i in xrange(N):
			for j in xrange(N):
				if arr[i][j] == 1:
					original[i][j] += 5
		arr = original

		############## BREADTH-FIRST SEARCH FOR SOLUTION ##################
		sol = list()
		solution_found = False
		q = Queue.Queue()
		q.put((0,deepcopy(arr)))

		while not solution_found:
			Nmoves, this = q.get()
			if Nmoves == 6:
				break
			for move in moves:
				new, solution_found = do_move(move, this)
				if solution_found:
					break
				q.put((Nmoves+1,new))
			optimal_moves = Nmoves+1

		############## OUTPUT #################
		optimal_moves = 50
		if not solution_found:
			d = {"N":N, "stars1":optimal_moves+4, "stars2":optimal_moves+2, "stars3":optimal_moves, 
					"dots":[], "blocks":[], "goals":[]}
			for i in range(N):
				for j in range(N):
					if arr[i][j] == -2:
						d["blocks"].append([i,j])
					elif arr[i][j] == 1:
						d["dots"].append([i,j])
					elif arr[i][j] == 5:
						d["goals"].append([i,j])
					elif arr[i][j] == 6:
						d["dots"].append([i,j])
						d["goals"].append([i,j])

			json.dump(d,open('s'+str(season)+'l'+str(level)+".txt", 'w'))
			print level
			level += 1