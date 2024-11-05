# 这是 fun mode，和一般的 XCPC 赛制有所不同：
# 1.罚时公式修改为：当前时间 + 10min * 当前的错误提交次数的平方，错误提交次数算上编译错误次数
# 2.一血队伍视作通过三道题，一血后的 30min 内通过该题的视作通过两道题
# 3.不进行封榜

import time

file=open("data.dat","r",encoding="utf-8") # data.dat 为 XCPCIO 上下载的数据，可替换为任意一场比赛，以 2024 ICPC 成都站为例
contest_name=file.readline()[10:-2] # 比赛名称
contest_length=int(file.readline()[9:]) # 比赛总时间（300）
problem_cnt=int(file.readline()[10:]) # 题目数，一般为 13
team_cnt=int(file.readline()[7:]) # 队伍数，但通常不准确，需要加以修正
submit_cnt=int(file.readline()[13:]) # 总提交数
problem_solved={} # 记录题目解决信息，便于处理一血
problem_solved_team={} # 记录哪些队伍解决了某题目，便于处理同一队伍多次通过某题目的情况
get_problem_id={} # 题目字母和数字转换
get_problem_chr={}
judge_CE={} # 记录CE提交的次数，修正罚时
get_team={} # 对队伍编号
team_state={} # 队伍状态，包括通过数和罚时
first_solve_time={} # 记录该题一血的时间戳


for i in range(problem_cnt): # 读入题目信息
    ch=file.readline()[3]
    problem_solved[ch]=0
    get_problem_id[ch]=i+1
    get_problem_chr[i+1]=ch
    first_solve_time[i+1]=0


flag=True # 记录是否已经处理完所有队伍
for i in range(team_cnt):
    str=file.readline().split("\"")[1]
    if str=="Пополнить команду": # 猜测是占位符，修正总队伍数并跳过处理
        if flag:
            team_cnt=i
        flag=False
    else:
        get_team[i+1]=str
        team_state[i+1]=[0,0]
        problem_solved_team[i+1]={}
        judge_CE[i+1]={}
        for j in range(problem_cnt):
            problem_solved_team[i+1][j+1]=0
            judge_CE[i+1][j+1]=0


AU=team_cnt//10 # 计算金牌线，下同
if team_cnt%10>0:
    AU+=1
AG=team_cnt*3//10
if team_cnt*3%10>0:
    AG+=1
CU=team_cnt*6//10
if team_cnt*6%10>0:
    CU+=1


list=[] # 读入提交列表
for i in range(submit_cnt):
    tmp=file.readline()[3:-1].split(",")
    team_id=int(tmp[0]) # 队伍的编号
    problem_id=tmp[1] # 队伍提交的题目编号
    cur_try=int(tmp[2]) # 队伍尝试该题的次数（包括CE）
    cur_time=int(tmp[3]) # 当前时间戳
    state=tmp[4] # 测评结果
    list.append({"team_id":team_id,"problem_id":problem_id,"cur_try":cur_try,"cur_time":cur_time,"state":state})
list.sort(key=lambda x:x["cur_time"]) # 对提交列表排序


cur_time=0 # 模拟当前时间戳
ind=0 # 当前提交队列的指针
print(contest_name)
for i in range(contest_length*60): # 模拟比赛提交队列情况

    if i%60==0: # 输出现在的时间（分钟）
        print(f"Time={i//60}")

    for j in range(problem_cnt):
        if 1501<i<=17700 and i-first_solve_time[j+1]==1501:
            print(f"距离{get_problem_chr[j+1]}题一血祝福结束还有 5min")
        if i>1801 and i-first_solve_time[j+1]==1801:
            print(f"{get_problem_chr[j+1]}题一血祝福已结束")


    while ind<submit_cnt and list[ind]["cur_time"]==i: # 处理所有当前时间戳的提交
        team_id=list[ind]["team_id"]
        problem_id=list[ind]["problem_id"]
        cur_try=list[ind]["cur_try"]
        cur_time=list[ind]["cur_time"]
        state=list[ind]["state"]
        team=get_team[team_id]
        ind+=1


        if state=="OK" and problem_solved_team[team_id][get_problem_id[problem_id]]==0: # 该队伍 AC 了这道题
            team_state[team_id][0]+=1
            problem_solved_team[team_id][get_problem_id[problem_id]]=1
            problem_solved[problem_id]+=1
            if problem_solved[problem_id]==1: # 一血队伍
                print(f"{problem_id}题一血已诞生！")
                team_state[team_id][0]+=2
                first_solve_time[get_problem_id[problem_id]]=cur_time;
            elif cur_time-first_solve_time[get_problem_id[problem_id]]<=1800:
                team_state[team_id][0]+=1
            team_state[team_id][1]+=cur_time//60+10*(cur_try-1)*(cur_try-1)


        rank=1
        for j in team_state: # O(n)判断目前排名
            if team_state[j][0]>team_state[team_id][0] or (team_state[j][0]==team_state[team_id][0] and team_state[j][1]<team_state[team_id][1]):
                rank+=1
        if rank<=AU:
            print(f"[Au]排名:{rank},(通过={team_state[team_id][0]},罚时={team_state[team_id][1]}),{team},第{cur_try}次提交{problem_id}题,{state}")
        elif rank<=AG:
            print(f"[Ag]排名:{rank},(通过={team_state[team_id][0]},罚时={team_state[team_id][1]}),{team},第{cur_try}次提交{problem_id}题,{state}")
        elif rank<=CU:
            print(f"[Cu]排名:{rank},(通过={team_state[team_id][0]},罚时={team_state[team_id][1]}),{team},第{cur_try}次提交{problem_id}题,{state}")
        else:
            print(f"[Fe]排名:{rank},(通过={team_state[team_id][0]},罚时={team_state[team_id][1]}),{team},第{cur_try}次提交{problem_id}题,{state}")


    time.sleep(1) # 模拟时间，等待 1 秒，可以注释掉()

valid=0
for i in team_state:
    if team_state[i][0]>0:
        valid+=1
AU=valid//10 # 用有效队伍数修正奖牌线
if valid%10>0:
    AU+=1
AG=valid*3//10
if valid*3%10>0:
    AG+=1
CU=valid*6//10
if valid*6%10>0:
    CU+=1

print("最终结果")
List=[] # 排名
List.append(None)
for i in team_state:
    List.append(None)
for i in team_state:
    rank=1
    for j in team_state:  # O(n)判断目前排名
        if team_state[j][0]>team_state[i][0] or (team_state[j][0]==team_state[i][0] and team_state[j][1]<team_state[i][1]):
            rank+=1
    R=rank
    while List[R]!=None: # 处理成绩一样的情况
        R+=1
    team=get_team[i]
    if rank<=AU:
        List[R]=f"[Au]排名:{rank},(通过={team_state[i][0]},罚时={team_state[i][1]}),{team}"
    elif rank<=AG:
        List[R]=f"[Ag]排名:{rank},(通过={team_state[i][0]},罚时={team_state[i][1]}),{team}"
    elif rank<=CU:
        List[R]=f"[Cu]排名:{rank},(通过={team_state[i][0]},罚时={team_state[i][1]}),{team}"
    else:
        List[R]=f"[Fe]排名:{rank},(通过={team_state[i][0]},罚时={team_state[i][1]}),{team}"
for i in team_state:
    print(List[i])
