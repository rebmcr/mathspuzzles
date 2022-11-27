import sys, random, datetime, itertools
import multiprocessing as mp

quick = False
reservedcores = 2

grid = [15,14,24,5,18,22,21,16,19,25,9,23,12,17,10,6,1,11,2,20,4,3,8]

pool = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

solvedgrids = []

def test1(candidate: list=grid) -> list:
    if ((candidate[0]*7)+candidate[1]-candidate[2]-candidate[3]) == 90:
        return [True, f"Valid row 1 found: {candidate[0]}×7+{candidate[1]}-{candidate[2]}-{candidate[3]} = 90\n"]
    else:
        return False

def test2(candidate: list=grid) -> list:
    if (13+candidate[4]+candidate[5]-candidate[6]+candidate[7]) == 48:
        return [True, f"Valid row 2 found: 13+{candidate[4]}+{candidate[5]}-{candidate[6]}+{candidate[7]} = 48\n"]
    else:
        return False

def test3(candidate: list=grid) -> list:
    if (candidate[8]+(candidate[9]*candidate[10])+candidate[11]-candidate[12]) == 255:
        return [True, f"Valid row 3 found: {candidate[8]}+{candidate[9]}×{candidate[10]}+{candidate[11]}-{candidate[12]} = 255\n"]
    else:
        return False

def test4(candidate: list=grid) -> list:
    if (candidate[13]+candidate[14]+candidate[15]+candidate[16]-candidate[17]) == 23:
        return [True, f"Valid row 4 found: {candidate[13]}+{candidate[14]}+{candidate[15]}+{candidate[16]}-{candidate[17]} = 23\n"]
    else:
        return False

def test5(candidate: list=grid) -> list:
    if ((candidate[18]*candidate[19]/candidate[20])-candidate[21]+candidate[22]) == 15:
        return [True, f"Valid row 5 found: {candidate[18]}×{candidate[19]}÷{candidate[20]}-{candidate[21]}+{candidate[22]} = 15\n"]
    else:
        return False

def test6(candidate: list=grid) -> list:
    if (candidate[0]-13+candidate[8]+(candidate[13]*candidate[18])) == 55:
        return [True, f"Valid column 1 found: {candidate[0]}-13+{candidate[8]}+{candidate[13]}×{candidate[18]} = 55\n"]
    else:
        return False

def test7(candidate: list=grid) -> list:
    if (7+(candidate[4]*candidate[9])-candidate[14]-candidate[19]) == 427:
        return [True, f"Valid column 2 found: 7+{candidate[4]}×{candidate[9]}-{candidate[14]}-{candidate[19]} = 427\n"]
    else:
        return False

def test8(candidate: list=grid) -> list:
    if ((candidate[1]*candidate[5])+candidate[10]+candidate[15]-candidate[20]) == 319:
        return [True, f"Valid column 3 found: {candidate[1]}×{candidate[5]}+{candidate[10]}+{candidate[15]}-{candidate[20]} = 319\n"]
    else:
        return False

def test9(candidate: list=grid) -> list:
    if (candidate[2]+candidate[6]+candidate[11]-candidate[16]+candidate[21]) == 70:
        return [True, f"Valid column 4 found: {candidate[2]}+{candidate[6]}+{candidate[11]}-{candidate[16]}+{candidate[21]} = 70\n"]
    else:
        return False

def test10(candidate: list=grid) -> list:
    if (candidate[3]-candidate[7]+candidate[12]+candidate[17]+candidate[22]) == 20:
        return [True, f"Valid column 5 found: {candidate[3]}-{candidate[7]}+{candidate[12]}+{candidate[17]}+{candidate[22]} = 20\n"]
    else:
        return False

def testall(candidate: list=grid) -> bool:
    # We do these in order of restrictiveness, so we can bail early
    if test7(candidate):
        if test6(candidate):
            if test1(candidate):
                if test8(candidate):
                    if test2(candidate):
                        if test3(candidate):
                            if test5(candidate):
                                if test9(candidate):
                                    if test10(candidate):
                                        if test4(candidate):
                                            return True
    return False

def testrows(candidate: list=grid) -> bool:
    # We do these in order of restrictiveness, so we can bail early
    if test1(candidate):
        if test2(candidate):
            if test3(candidate):
                if test5(candidate):
                    if test4(candidate):
                        return True
    return False

def testcols(candidate: list=grid) -> bool:
    # We do these in order of restrictiveness, so we can bail early
    if test7(candidate):
        if test6(candidate):
            if test8(candidate):
                if test9(candidate):
                    if test10(candidate):
                        return True
    return False

def testid(id: int, candidate: list=grid) -> list:
    if id == 1:
        return test1(candidate)
    elif id == 2:
        return test2(candidate)
    elif id == 3:
        return test3(candidate)
    elif id == 4:
        return test4(candidate)
    elif id == 5:
        return test5(candidate)
    elif id == 6:
        return test6(candidate)
    elif id == 7:
        return test7(candidate)
    elif id == 8:
        return test8(candidate)
    elif id == 9:
        return test9(candidate)
    elif id == 10:
        return test10(candidate)

def dumb():
    count = 0
    limit = 1000000000
    while count < limit:
        if testall():
            render()
            sys.exit(0)
        else:
            random.shuffle(grid)
            count += 1
            if count%100000 == 0:
                print(f"Attempts so far:{count}")
    print(f"Giving up random search after {limit} attempts.")

def batch4(a: int,b: int,c: int,d: int,id: int,title: str,avoids: list=[7,13]) -> str:
    count = 0
    grid[a] = 1
    invalids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    message = ''
    while grid[a]<25:
        grid[b] = grid[a]+1
        if grid[b] == 26:
            grid[b] = 1
        while grid[b] != grid[a]:
            grid[c] = grid[b]+1
            if grid[c] == 26:
                grid[c] = 1
            while grid[c] != grid[b]:
                grid[d] = grid[c]+1
                if grid[d] == 26:
                    grid[d] = 1
                while grid[d] != grid[c]:
                    if (grid[d]==grid[c]) or (grid[d]==grid[b]) or (grid[d]==grid[a]) or (grid[c]==grid[b]) or (grid[c]==grid[a]) or (grid[b]==grid[a]):
                        pass
                    elif (grid[d] in avoids) or (grid[c] in avoids) or (grid[b] in avoids) or (grid[a] in avoids):
                        pass
                    else:
                        result = testid(id)
                        if result:
                            count += 1
                            message += result[1]
                            while grid[d] in invalids:
                                invalids.remove(grid[d])
                            while grid[c] in invalids:
                                invalids.remove(grid[c])
                            while grid[b] in invalids:
                                invalids.remove(grid[b])
                            while grid[a] in invalids:
                                invalids.remove(grid[a])
                    grid[d]+=1
                    if grid[d] == 26:
                        grid[d] = 1
                grid[c]+=1
                if grid[c] == 26:
                    grid[c] = 1
            grid[b]+=1
            if grid[b] == 26:
                grid[b] = 1
        grid[a]+=1
    message += f"Finished search for {title}. Found {count} valid solutions. These numbers do not appear in {title}'s blank spaces: {invalids}.\n"
    return message

def batch5(a: int,b: int,c: int,d: int,e: int,id: int,title: str,avoids: list=[7,13]) -> str:
    count = 0
    grid[a] = 1
    invalids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    message = ''
    while grid[a]<25:
        grid[b] = grid[a]+1
        if grid[b] == 26:
            grid[b] = 1
        while grid[b] != grid[a]:
            grid[c] = grid[b]+1
            if grid[c] == 26:
                grid[c] = 1
            while grid[c] != grid[b]:
                grid[d] = grid[c]+1
                if grid[d] == 26:
                    grid[d] = 1
                while grid[d] != grid[c]:
                    grid[e] = grid[d]+1
                    if grid[e] == 26:
                        grid[e] = 1
                    while grid[e] != grid[d]:
                        if (grid[e]==grid[d]) or (grid[e]==grid[c]) or (grid[e]==grid[b]) or (grid[e]==grid[a]) or (grid[d]==grid[c]) or (grid[d]==grid[b]) or (grid[d]==grid[a]) or (grid[c]==grid[b]) or (grid[c]==grid[a]) or (grid[b]==grid[a]):
                            pass
                        elif (grid[e] in avoids) or (grid[d] in avoids) or (grid[c] in avoids) or (grid[b] in avoids) or (grid[a] in avoids):
                            pass
                        else:
                            result = testid(id)
                            if result:
                                count+=1
                                message += result[1]
                                while grid[e] in invalids:
                                    invalids.remove(grid[e])
                                while grid[d] in invalids:
                                    invalids.remove(grid[d])
                                while grid[c] in invalids:
                                    invalids.remove(grid[c])
                                while grid[b] in invalids:
                                    invalids.remove(grid[b])
                                while grid[a] in invalids:
                                    invalids.remove(grid[a])
                        grid[e]+=1
                        if grid[e] == 26:
                            grid[e] = 1
                    grid[d]+=1
                    if grid[d] == 26:
                        grid[d] = 1
                grid[c]+=1
                if grid[c] == 26:
                    grid[c] = 1
            grid[b]+=1
            if grid[b] == 26:
                grid[b] = 1
        grid[a]+=1
    message += f"Finished search for {title}. Found {count} valid solutions. These numbers do not appear in {title}'s blank spaces: {invalids}.\n"
    return message

def searchrow1() -> str:
    return batch4(0,1,2,3,1,'row 1')

def searchrow2() -> str:
    return batch4(4,5,6,7,2,'row 2')

def searchrow3() -> str:
    return batch5(8,9,10,11,12,3,'row 3')

def searchrow4() -> str:
    return batch5(13,14,15,16,17,4,'row 4')

def searchrow5() -> str:
    return batch5(18,19,20,21,22,5,'row 5')

def searchcol1() -> str:
    return batch4(0,8,13,18,6,'column 1')

def searchcol2() -> str:
    return batch4(4,9,14,19,7,'column 2')

def searchcol3() -> str:
    return batch5(1,5,10,15,20,8,'column 3')

def searchcol4() -> str:
    return batch5(2,6,11,16,21,9,'column 4')

def searchcol5() -> str:
    return batch5(3,7,12,17,22,10,'column 5')

def searchid(id: int) -> str:
    if id == 1:
        return searchrow1()
    elif id == 2:
        return searchrow2()
    elif id == 3:
        return searchrow3()
    elif id == 4:
        return searchrow4()
    elif id == 5:
        return searchrow5()
    elif id == 6:
        return searchcol1()
    elif id == 7:
        return searchcol2()
    elif id == 8:
        return searchcol3()
    elif id == 9:
        return searchcol4()
    elif id == 10:
        return searchcol5()
    else:
        return False

def searchall() -> str:
    out = searchrow1() #  Finds  1144 solutions
    out += searchrow2() # Finds  4470 solutions
    out += searchrow3() # Finds  6200 solutions
    out += searchrow4() # Finds 59184 solutions
    out += searchrow5() # Finds 10482 solutions
    out += searchcol1() # Finds   904 solutions
    out += searchcol2() # Finds   132 solutions
    out += searchcol3() # Finds  4358 solutions
    out += searchcol4() # Finds 17502 solutions
    out += searchcol5() # Finds 49860 solutions
    return out

def chain4(a: int,b: int,c: int,d: int,test: int,avoids: list=[7,13]) -> list:
    mygrid = grid.copy()
    valids = []
    poola = pool.copy()
    for n in avoids:
        poola.remove(n)
    ia = 0
    while ia<len(poola):
        mygrid[a] = poola[ia]
        poolb = poola.copy()
        poolb.remove(mygrid[a])
        ib = 0
        while ib<len(poolb):
            mygrid[b] = poolb[ib]
            poolc = poolb.copy()
            poolc.remove(mygrid[b])
            ic = 0
            while ic<len(poolc):
                mygrid[c] = poolc[ic]
                poold = poolc.copy()
                poold.remove(mygrid[c])
                id = 0
                while id<len(poold):
                    mygrid[d] = poold[id]
                    result = testid(test, mygrid)
                    if result:
                        valids.append([mygrid[a],mygrid[b],mygrid[c],mygrid[d]])
                    id+=1
                ic+=1
            ib+=1
        ia+=1
    return valids

def chain5(a: int,b: int,c: int,d: int,e: int,test: int,avoids: list=[7,13]) -> list:
    mygrid = grid.copy()
    valids = []
    poola = pool.copy()
    for n in avoids:
        poola.remove(n)
    ia = 0
    while ia<len(poola):
        mygrid[a] = poola[ia]
        poolb = poola.copy()
        poolb.remove(mygrid[a])
        ib = 0
        while ib<len(poolb):
            mygrid[b] = poolb[ib]
            poolc = poolb.copy()
            poolc.remove(mygrid[b])
            ic = 0
            while ic<len(poolc):
                mygrid[c] = poolc[ic]
                poold = poolc.copy()
                poold.remove(mygrid[c])
                id = 0
                while id<len(poold):
                    mygrid[d] = poold[id]
                    poole = poold.copy()
                    poole.remove(mygrid[d])
                    ie = 0
                    while ie<len(poole):
                        mygrid[e] = poole[ie]
                        result = testid(test, mygrid)
                        if result:
                            valids.append([mygrid[a],mygrid[b],mygrid[c],mygrid[d],mygrid[e]])
                        ie+=1
                    id+=1
                ic+=1
            ib+=1
        ia+=1
    return valids

def iterid(id: int,avoids: list=[7,13]) -> list:
    if id == 1: # row1
        return chain4(0,1,2,3,1,avoids)
    elif id == 2: # row2
        return chain4(4,5,6,7,2,avoids)
    elif id == 3: # row3
        return chain5(8,9,10,11,12,3,avoids)
    elif id == 4: # row4
        return chain5(13,14,15,16,17,4,avoids)
    elif id == 5: # row5
        return chain5(18,19,20,21,22,5,avoids)
    elif id == 6: # col1
        return chain4(0,8,13,18,6,avoids)
    elif id == 7: # col2
        return chain4(4,9,14,19,7,avoids)
    elif id == 8: # col3
        return chain5(1,5,10,15,20,8,avoids)
    elif id == 9: # col4
        return chain5(2,6,11,16,21,9,avoids)
    elif id == 10: # col5
        return chain5(3,7,12,17,22,10,avoids)
    else:
        return False

def render(agrid: list=grid):
    print(
        f" {agrid[0]: ^3} ×  7  + {agrid[1]: ^3} - {agrid[2]: ^3} - {agrid[3]: ^3} =  90\n"
        '  -     +     ×     +     -\n'
        f" 13  + {agrid[4]: ^3} + {agrid[5]: ^3} - {agrid[6]: ^3} + {agrid[7]: ^3} =  48\n"
        '  +     ×     +     +     +\n'
        f" {agrid[8]: ^3} + {agrid[9]: ^3} × {agrid[10]: ^3} + {agrid[11]: ^3} - {agrid[12]: ^3} = 255\n"
        '  +     -     +     -     +\n'
        f" {agrid[13]: ^3} + {agrid[14]: ^3} + {agrid[15]: ^3} + {agrid[16]: ^3} - {agrid[17]: ^3} =  23\n"
        '  ×     -     -     +     +\n'
        f" {agrid[18]: ^3} × {agrid[19]: ^3} ÷ {agrid[20]: ^3} - {agrid[21]: ^3} + {agrid[22]: ^3} =  15\n"
        '  =     =     =     =     =\n'
        " 55    427   319   70    20"
    )

def brute(mode: int=0):
    # Order of preference (columnwise): col2, col1, col3, col4, col5 (7, 6, 8, 9, 10)
    # Order of preference (rowwise): row1, row2, row3, row5, row4 (1, 2, 3, 5, 4)
    # Order of preference (fully integrated): col2, col1, row1, col3, row2, row3, row5, col4, col5, row4 (7, 6, 1, 8, 2, 3, 5, 9, 10, 4)
    global solvedgrids
    if mode == 0: # columnwise
        print(f"Starting search at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        col2 = iterid(7)
        if col2:
            print(f"Generated {len(col2)} top-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            cores = mp.cpu_count() - reservedcores
            pools = [[] for _ in range(cores)]
            for e, pool in zip(col2, itertools.cycle(pools)):
                pool.append(e)
            counts = []
            for pool in pools:
                if len(pool) not in counts:
                    counts.append(len(pool))
            counts.sort()
            if len(counts) == 1:
                print(f"CPU count: {cores + reservedcores}. We will spawn {cores} worker processes, with {counts[0]} solutions each.")
            elif len(counts) == 2:
                print(f"CPU count: {cores + reservedcores}. We will spawn {cores} worker processes, with {counts[0]} or {counts[1]} solutions each.")
            else:
                print(f"CPU count: {cores + reservedcores}. We will spawn {cores} worker processes, with roughly {counts[0]} solutions each.")
            procs = []
            rxs = []
            txs = []
            for i in range(cores):
                rx, tx = mp.Pipe()
                rxs.append(rx)
                txs.append(tx)
                procs.append(mp.Process(target=bruteworker, args=(pools[i], txs[i])))
            for proc in procs:
                proc.start()
            while mp.active_children():
                for rx in rxs:
                    if rx.poll():
                        obj = rx.recv()
                        if isinstance(obj, str):
                            print(obj)
                        elif isinstance(obj, list):
                            solvedgrids.append(obj)
                            print(f"    {len(solvedgrids)} solutions found so far.")
                            if quick:
                                print(f"One solution is good enough, rendering valid grid at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                render(solvedgrids[0])
                                for proc in procs:
                                    proc.kill()
                                sys.exit(0)
            print(f"Workers done at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{len(solvedgrids)} total solutions found!!!")
        print(f"Rendering valid grid(s) at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for solution in solvedgrids:
            if testall(solution):
                render(solution)
            else:
                print('Error: a solution was falsely branded correct:')
                print(solution)
        print(f"Ending run at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        sys.exit(0)
    elif mode == 1: # rowwise
        print('Not implemented yet.')
        sys.exit(1)
    elif mode == 2: # integrated
        print('Not sure if I am even smart enough implement this one.')
        sys.exit(2)
    else:
        print(f"Error: search mode {mode} not valid.")
        sys.exit(65535)

def bruteworker(col2: list, tx):
    myname = mp.current_process().name
    size2 = len(col2)
    count2 = 0
    tx.send(f" {myname} received {size2} first-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for set2 in col2:
        avoids = [7,13,set2[0],set2[1],set2[2],set2[3]]
        col1 = iterid(6, avoids)
        if col1:
            size1 = len(col1)
            count1 = 0
            tx.send(f" {myname} generated {size1} second-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            for set1 in col1:
                avoids = [7,13,set2[0],set2[1],set2[2],set2[3],set1[0],set1[1],set1[2],set1[3]]
                col3 = iterid(8, avoids)
                if col3:
                    #size3 = len(col3)
                    #count3 = 0
                    #tx.send(f"  {myname} generated {size3} third-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    for set3 in col3:
                        avoids = [7,13,set2[0],set2[1],set2[2],set2[3],set1[0],set1[1],set1[2],set1[3],set3[0],set3[1],set3[2],set3[3],set3[4]]
                        col4 = iterid(9, avoids)
                        if col4: # fast from here, no messaging spam
                            for set4 in col4:
                                avoids = [7,13,set2[0],set2[1],set2[2],set2[3],set1[0],set1[1],set1[2],set1[3],set3[0],set3[1],set3[2],set3[3],set3[4],set4[0],set4[1],set4[2],set4[3],set4[4]]
                                col5 = iterid(10, avoids)
                                if col5:
                                    for set5 in col5:
                                        candidate = [set1[0],set3[0],set4[0],set5[0],set2[0],set3[1],set4[1],set5[1],set1[1],set2[1],set3[2],set4[2],set5[2],set1[2],set2[2],set3[3],set4[3],set5[3],set1[3],set2[3],set3[4],set4[4],set5[4]]
                                        if testrows(candidate):
                                            tx.send(candidate)
                        #count3 += 1
                        #tx.send(f" {myname} completed {count3} of {size3} third-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                count1 += 1
                tx.send(f" {myname} completed {count1} of {size1} second-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        count2 += 1
        tx.send(f" {myname} completed {count2} of {size2} first-layer solutions at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    dumb()
