import matplotlib.pyplot as plt

file=open("data.dat","r",encoding="utf-8") # data.dat 为 XCPCIO 上下载的数据，可替换为任意一场比赛，以 2024 ICPC 成都站为例
contest_name=file.readline()[10:-2] # 比赛名称
contest_length=int(file.readline()[9:]) # 比赛总时间（300）
problem_cnt=int(file.readline()[10:]) # 题目数，一般为 13
team_cnt=int(file.readline()[7:]) # 队伍数，但通常不准确，需要加以修正
submit_cnt=int(file.readline()[13:]) # 总提交数，但有可能不准确
problem_solved={} # 记录题目解决信息，便于处理一血
problem_solved_team={} # 记录哪些队伍解决了某题目，便于处理同一队伍多次通过某题目的情况
get_problem_id={} # 题目字母和数字转换
judge_CE={} # 记录CE提交的次数，修正罚时
frozen_state={}
get_team={} # 对队伍编号
team_state={} # 队伍状态，包括通过数和罚时

AC=[0]*300
TOTAL=[0]*300
TIME=[0]*300


for i in range(problem_cnt): # 读入题目信息
    ch=file.readline()[3]
    problem_solved[ch]=0
    get_problem_id[ch]=i+1


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
        frozen_state[i+1]=[0,0]
        problem_solved_team[i+1]={}
        judge_CE[i+1]={}
        for j in range(problem_cnt):
            problem_solved_team[i+1][j+1]=0
            judge_CE[i+1][j+1]=0


list=[] # 读入提交列表
for i in range(submit_cnt):
    str=file.readline()
    if len(str)<=3: # 如果没有读到东西
        submit_cnt=i
        break
    tmp=str[3:-1].split(",")
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
frozen=False # 是否封榜
for i in range(contest_length*60): # 模拟比赛提交队列情况

    while ind<submit_cnt and list[ind]["cur_time"]==i: # 处理所有当前时间戳的提交
        team_id=list[ind]["team_id"]
        problem_id=list[ind]["problem_id"]
        cur_try=list[ind]["cur_try"]-judge_CE[team_id][get_problem_id[problem_id]] # 减去 CE 的影响
        cur_time=list[ind]["cur_time"]//60 # 罚时精确到分钟
        state=list[ind]["state"]
        team=get_team[team_id]
        ind+=1

        TOTAL[i//60]+=1

        if state=="OK" and problem_solved_team[team_id][get_problem_id[problem_id]]==0: # 该队伍 AC 了这道题
            problem_solved_team[team_id][get_problem_id[problem_id]]=1
            AC[i//60]+=1

for i in range(1,300):
    TIME[i]=i

plt.rcParams['font.family']='Times New Roman, SimSun'

plt.figure(figsize=(20, 10))

plt.plot(TOTAL,color='blue')
plt.title(contest_name+' 赛时提交频率')
plt.xlabel('时间')
plt.ylabel('提交数')
plt.grid(True)
plt.xticks(range(0,contest_length+1,15))
plt.show()

plt.figure(figsize=(20, 10))
plt.plot(AC,color='green')
plt.title(contest_name+' 赛时每分钟的有效AC数')
plt.xlabel('时间')
plt.ylabel('有效AC提交')
plt.grid(True)
plt.xticks(range(0,contest_length+1,15))
plt.show()
