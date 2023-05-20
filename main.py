from tkinter import filedialog
from rf.trainModel import *
from mlp.deepLearn import *
from Logger import *
from tkinter import *


def run_NN_train(result_listbox):
    result_listbox.delete(0, END)
    wait_window = Toplevel()
    wait_window.title("请稍候...")
    wait_window.geometry("300x100")
    wait_window.resizable(False, False)
    # 将焦点锁定在等待提示框上，禁止用户点击主窗口
    wait_window.grab_set()
    # 将等待提示框提升到所有窗口的最前面
    wait_window.lift()
    # 创建等待提示框的Label
    wait_label = Label(wait_window, text="请稍候...", font=("Arial", 20))
    wait_label.pack(pady=20)
    # 禁用等待提示框的关闭按钮
    wait_window.protocol("WM_DELETE_WINDOW", lambda: None)

    # 提取所以待检测文件的特征值
    thread_NN_check = Thread(target=NN_train(result_listbox))
    thread_NN_check.start()

    # 在等待提示框中显示提示信息
    while thread_NN_check.is_alive():
        wait_label.config(text="检测中，请不要点击😊")
        wait_window.update_idletasks()

    # 关闭等待提示框并释放焦点锁定
    wait_window.destroy()

def NN_train(result_listbox):

    trainRes=dL.dltrain(Norfiletrain_name,Shellfiletrain_name,createmodel_name)
    print(f'{Norfiletrain_name},{Shellfiletrain_name},{createmodel_name}')
    for i in trainRes:
        result_listbox.insert(END, i)



def run_NN_check(result_listbox):
    # 先清空结果列表
    result_listbox.delete(0, END)
    wait_window = Toplevel()
    wait_window.title("请稍候...")
    wait_window.geometry("300x100")
    wait_window.resizable(False, False)
    # 将焦点锁定在等待提示框上，禁止用户点击主窗口
    wait_window.grab_set()
    # 将等待提示框提升到所有窗口的最前面
    wait_window.lift()
    # 创建等待提示框的Label
    wait_label = Label(wait_window, text="请稍候...", font=("Arial", 20))
    wait_label.pack(pady=20)
    # 禁用等待提示框的关闭按钮
    wait_window.protocol("WM_DELETE_WINDOW", lambda: None)

    # 提取所有待检测文件的特征值
    thread_NN_check = Thread(target= NN_check(result_listbox))
    thread_NN_check.start()

    # 在等待提示框中显示提示信息
    while thread_NN_check.is_alive():
        wait_label.config(text="检测中，请不要点击😊")
        wait_window.update_idletasks()

    # 关闭等待提示框并释放焦点锁定
    wait_window.destroy()

def NN_check(result_listbox):
    """
    获取预测值 文件名列表
    :param result_listbox:
    :return:
    """
    global checked_filename

    # 模型预测
    predict_result,checked_filename=dL.dltest(filecheck_name,loadmodel_name)


    # 将模型预测结果整理并输出到UI界面
    for i in range(len(checked_filename)):
        if predict_result[i] == 0:
            temp_result=str(i+1)+":"+checked_filename[i]+" is normal"
            print(temp_result)
            result_listbox.insert(END,temp_result)
        elif predict_result[i] == 1:
            temp_result=str(i+1)+":"+checked_filename[i]+ " is webshell"
            print(temp_result)
            result_listbox.insert(END, temp_result)

def select_file(setfile):
    global loadmodel_name
    filename=filedialog.askopenfilename()
    setfile.set(filename)
    loadmodel_name=setfile.get()

def select_path(setpath):
    global filecheck_name
    file_path=filedialog.askdirectory()
    setpath.set(file_path)
    filecheck_name=setpath.get()

def NN_select_Nor_path(setpath):
    global Norfiletrain_name
    file_path=filedialog.askdirectory()
    setpath.set(file_path)
    Norfiletrain_name=setpath.get()
    print(Norfiletrain_name)

def NN_select_Shell_path(setpath):
    global Shellfiletrain_name
    file_path=filedialog.askdirectory()
    setpath.set(file_path)
    Shellfiletrain_name=setpath.get()
    print(Shellfiletrain_name)
def NNtrain_select_modelsavepath(model_savepath_text):
    global createmodel_name
    model_savepath=filedialog.asksaveasfilename(defaultextension='.pth', filetypes=[('pth Files', '*.pth'), ('All Files', '*.*')])
    model_savepath_text.set(model_savepath)
    createmodel_name=model_savepath_text.get()
    print(createmodel_name)












def check(result_listbox):
    """
    预测
    """
    # 加载模型
    rfc=joblib.load(loadmodel_name)

    # 模型预测
    predict_result=rfc.predict(pre_feature_value)

    # 将模型预测结果整理并输出到UI界面
    for i in range(len(checked_filename)):
        if predict_result[i] == 0:
            temp_result=str(i+1)+":"+checked_filename[i]+" is normal"
            print(temp_result)
            result_listbox.insert(END,temp_result)
        elif predict_result[i] == 1:
            temp_result=str(i+1)+":"+checked_filename[i]+ " is webshell"
            print(temp_result)
            result_listbox.insert(END,temp_result)

# 获取特征值
def get_feature():
    """
    获取数据 不用存pickle了
    """
    global pre_feature_value,checked_filename
    # 踩坑了，要记得先清空，不然第二次调用会存在旧值。
    pre_feature_value=[]
    checked_filename=[]
    for filename, fullpath in filelist.items():
        # 觉得还是做一个文件后缀检测提高效率比较好
        (_, extension) = os.path.splitext(fullpath)
        if extension == ".php":
            try:

                # 获取静态统计特征
                entropy, ic, evilfunctions = trainmodel.run_getStaticFeature(fullpath)
                # 获取动态opcode特征
                textrank_value = trainmodel.run_getDynamicFeature(fullpath)
                # 整合汇总后加入到预处理训练集合中

                temp_value = []
                # 92个opcode动态特征值
                for tv in textrank_value:
                    temp_value.append(tv)
                # 6个静态统计特征值
                temp_value.append(entropy)
                temp_value.append(ic)
                for ef in evilfunctions:
                    temp_value.append(ef)
                pre_feature_value.append(temp_value)
                # 顺便存个文件名
                checked_filename.append(fullpath)
            except:
                print(filename + " error!")
                continue
        else:
            continue

# 读取目录下的所有文件
def fileread(filepath):
    global filelist
    for root, dirs, files in os.walk(filepath):
        # print(root,dirs,files)
        for filename in files:
            filepath = os.path.join(root, filename)
            filelist[filename] = filepath
        # print(filelist)

# 日志功能
def log():
    # 自定义目录存放日志文件
    log_path = './Logs/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    # 日志文件名按照程序运行时间设置
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    # 记录 traceback 异常信息
    sys.stderr = Logger(log_file_name)

def RFCcheck_select_path(setpath):
    global filecheck_name
    file_path=filedialog.askdirectory()
    setpath.set(file_path)
    filecheck_name=setpath.get()

def RFCcheck_select_file(setfile):
    global loadmodel_name
    filename=filedialog.askopenfilename()
    setfile.set(filename)
    loadmodel_name=setfile.get()

def RFCtrain_select_modelsavepath(model_savepath_text):
    model_savepath=filedialog.asksaveasfilename(defaultextension='.pkl', filetypes=[('pikle Files', '*.pkl'), ('All Files', '*.*')])
    model_savepath_text.set(model_savepath)
    trainmodel.createmodel_name=model_savepath_text.get()

def RFCtrain_select_traindatapath(model_traindata_text):
    traindata_path=filedialog.askdirectory()
    model_traindata_text.set(traindata_path)
    trainmodel.fileread_name=model_traindata_text.get()

# 这里是主要的随机森林检测运行模块,还是得把result_listbox传过来才行。
def run_check(result_listbox):
    # 先清空结果列表
    result_listbox.delete(0, END)

    # 下面这一大段都是弹出等待提示不要点击
    # 创建Toplevel窗口作为等待提示框
    wait_window = Toplevel()
    wait_window.title("请稍候...")
    wait_window.geometry("300x100")
    wait_window.resizable(False, False)
    # 将焦点锁定在等待提示框上，禁止用户点击主窗口
    wait_window.grab_set()
    # 将等待提示框提升到所有窗口的最前面
    wait_window.lift()
    # 创建等待提示框的Label
    wait_label = Label(wait_window, text="请稍候...", font=("Arial", 20))
    wait_label.pack(pady=20)
    # 禁用等待提示框的关闭按钮
    wait_window.protocol("WM_DELETE_WINDOW", lambda: None)

    # 获取需要检测的文件夹的所有文件
    fileread(filecheck_name)
    # 提取所以待检测文件的特征值
    thread_get_feature = Thread(target=get_feature)
    thread_get_feature.start()
    # 在等待提示框中显示提示信息
    while thread_get_feature.is_alive():
        wait_label.config(text="检测中，请不要点击😊")
        wait_window.update_idletasks()

    # 检测启动
    check(result_listbox)

    # 关闭等待提示框并释放焦点锁定
    wait_window.destroy()
    # root_window.grab_release()

def run_tkinter_NNtrain():

    global photo
    model_savepath_text = StringVar()
    model_Nortraindata_text = StringVar()
    model_Shelltraindata_text = StringVar()
    predict_result = StringVar()

    # 首先隐藏父窗口
    root.withdraw()
    # 然后就是当前窗口的一些设置
    RFCtrain_window = Toplevel(root)
    RFCtrain_window.geometry('1005x592')
    RFCtrain_window.resizable(False, False)
    RFCtrain_window.attributes("-alpha", 0.9)
    RFCtrain_window.iconbitmap("img/scout.ico")

    # 剩下的事情就是在一个canvas画布上展开的了。
    photo = PhotoImage(file="img/9.png")
    # 画布
    canvas = Canvas(RFCtrain_window, width=1005, height=592)
    canvas.pack()
    # 背景
    canvas.create_image(0, 0, image=photo, anchor=NW)
    # 大标题&提示
    canvas.create_text(500, 40, text="神经网络训练模块", font=('华文行楷', 40, 'bold'))
    # canvas.create_text(500, 80, text="（训练数据路径需要先建立black-traindata和white-traindata两个目录！）", font=('楷体', 20, 'bold'),
    #                    fill="red")

    # 随机森林训练模块的主要控件
    model_savepath_button = Button(canvas, text="模型保存路径", font=('华文行楷', 20, 'bold'),
                                   command=lambda: NNtrain_select_modelsavepath(model_savepath_text))
    canvas.create_window(130, 120, window=model_savepath_button)

    model_savepath_entry = Entry(canvas, textvariable=model_savepath_text)
    canvas.create_window(250, 120, width=740, height=40, window=model_savepath_entry, anchor=W)


    model_Nortraindata_button = Button(canvas, text="正常数据路径", font=('华文行楷', 20, 'bold'),
                                    command=lambda: NN_select_Nor_path(model_Nortraindata_text))
    canvas.create_window(130, 190, window=model_Nortraindata_button)

    model_Nortraindat_entry = Entry(canvas, textvariable=model_Nortraindata_text)
    canvas.create_window(250, 190, width=740, height=40, window=model_Nortraindat_entry, anchor=W)


    model_Shelltraindata_button = Button(canvas, text="恶意数据路径", font=('华文行楷', 20, 'bold'),
                                    command=lambda: NN_select_Shell_path(model_Shelltraindata_text))
    canvas.create_window(130, 260, window=model_Shelltraindata_button)

    model_Shelltraindata_entry = Entry(canvas, textvariable=model_Shelltraindata_text)
    canvas.create_window(250, 260, width=740, height=40, window=model_Shelltraindata_entry, anchor=W)

    begintrain_button = Button(canvas, text="开始训练", font=('华文行楷', 20, 'bold'),
                               command=lambda: run_NN_train(predict_result_listbox))
    canvas.create_window(130, 330, window=begintrain_button)

    canvas.create_text(600, 330, text="模型训练结果:", font=('华文行楷', 30, 'bold'))

    predict_result_listbox = Listbox(canvas, listvariable=predict_result)
    canvas.create_window(30, 478, width=960, height=200, window=predict_result_listbox, anchor=W)

    # 添加关闭事件
    RFCtrain_window.protocol("WM_DELETE_WINDOW", lambda: close_second_window(RFCtrain_window))

def run_tkinter_NNcheck():
    global photo
    # RFCcheck中entry和listbox的值
    result = StringVar()
    model_text = StringVar()
    filelist_text = StringVar()
    # 首先隐藏父窗口
    root.withdraw()

    NNcheck_window = Toplevel(root)
    NNcheck_window.geometry('1005x592')
    NNcheck_window.resizable(False, False)
    NNcheck_window.attributes("-alpha", 1) # 透明度的值:0~1 也可以是小数点，0：全透明；1：全不透明
    NNcheck_window.iconbitmap("img/scout.ico")

    photo = PhotoImage(file="img/9.png")
    #添加画布
    canvas = Canvas(NNcheck_window, width=1005, height=592)
    canvas.pack()
    # 背景
    canvas.create_image(0, 0, image=photo, anchor=NW)
    # 大标题
    canvas.create_text(500, 40, text="神经网络检测模块", font=('华文行楷', 40, 'bold'))

    # 选择检测路径按钮&选中检测路径后展示文本框
    select_check_button = Button(canvas, text="选择检测路径", font=('华文行楷', 20, 'bold'),
                                 command=lambda: select_path(filelist_text))
    canvas.create_window(150, 120, window=select_check_button)
    select_entry = Entry(canvas, textvariable=filelist_text)
    canvas.create_window(20, 170, width=960, height=30, window=select_entry, anchor=W)

    # 选择模型路径按钮&选中模型路径后展示文本框
    select_model_button = Button(canvas,text="加载模型路径", font=('华文行楷', 20, 'bold'),command=lambda :select_file(model_text))
    canvas.create_window(500, 120, window=select_model_button)
    model_entry = Entry(canvas,textvariable=model_text)
    canvas.create_window(20, 205, width=960, height=30, window=model_entry, anchor=W)


    print(loadmodel_name)
    print(filecheck_name)
    # 检测结果列表
    result_listbox = Listbox(canvas, listvariable=result)
    canvas.create_window(20, 420, width=960, height=300, window=result_listbox, anchor=W)
    # 检测按钮
    check_button = Button(canvas, text="开始检测", font=('华文行楷', 20, 'bold'), command=lambda: run_NN_check(result_listbox))
    canvas.create_window(850, 120, window=check_button)
    # 检测结果标题
    canvas.create_text(500, 245, text="检测结果", font=('华文行楷', 30, 'bold'))

    # 添加关闭事件
    NNcheck_window.protocol("WM_DELETE_WINDOW", lambda: close_second_window(NNcheck_window))

def run_tkinter_RFCtrain():
    print("随机森林训练模块")
    global photo
    model_savepath_text=StringVar()
    model_traindata_text=StringVar()
    predict_result=StringVar()

    # 首先隐藏父窗口
    root.withdraw()
    # 然后就是当前窗口的一些设置
    RFCtrain_window = Toplevel(root)
    RFCtrain_window.geometry('1005x592')
    RFCtrain_window.resizable(False, False)
    RFCtrain_window.attributes("-alpha", 0.9)
    RFCtrain_window.iconbitmap("img/scout.ico")

    # 剩下的事情就是在一个canvas画布上展开的了。
    photo = PhotoImage(file="img/9.png")
    # 画布
    canvas = Canvas(RFCtrain_window, width=1005, height=592)
    canvas.pack()
    # 背景
    canvas.create_image(0, 0, image=photo, anchor=NW)
    # 大标题&提示
    canvas.create_text(500, 40, text="随机森林训练模块", font=('华文行楷', 40, 'bold'))
    canvas.create_text(500, 80, text="（训练数据路径需要先建立black-traindata和white-traindata两个目录！）", font=('楷体', 20, 'bold'),fill="red")

    # 随机森林训练模块的主要控件
    model_savepath_button=Button(canvas,text="模型保存路径", font=('华文行楷', 20, 'bold'),command=lambda :RFCtrain_select_modelsavepath(model_savepath_text))
    canvas.create_window(130, 120, window=model_savepath_button)
    model_savepath_entry = Entry(canvas, textvariable=model_savepath_text)
    canvas.create_window(250, 120, width=740, height=40, window=model_savepath_entry, anchor=W)
    model_traindata_button=Button(canvas,text="训练数据路径",font=('华文行楷', 20, 'bold'),command=lambda:RFCtrain_select_traindatapath(model_traindata_text))
    canvas.create_window(130,190,window=model_traindata_button)
    model_traindata_entry=Entry(canvas,textvariable=model_traindata_text)
    canvas.create_window(250,190,width=740, height=40,window=model_traindata_entry,anchor=W)
    begintrain_button=Button(canvas,text="开始训练",font=('华文行楷', 20, 'bold'),command=lambda:trainmodel.run_trainModel(predict_result_listbox))
    canvas.create_window(130,260,window=begintrain_button)
    canvas.create_text(600,260,text="模型预测训练数据的结果分析展示",font=('华文行楷', 30, 'bold'))
    predict_result_listbox = Listbox(canvas, listvariable=predict_result)
    canvas.create_window(30, 438, width=960, height=280, window=predict_result_listbox, anchor=W)



    # 添加关闭事件
    RFCtrain_window.protocol("WM_DELETE_WINDOW", lambda: close_second_window(RFCtrain_window))



# 随机森林检测模块图形化界面主程序
def run_tkinter_RFCcheck():
    print("随机森林检测模块")
    global photo
    # RFCcheck中entry和listbox的值
    result = StringVar()
    model_text = StringVar()
    filelist_text = StringVar()

    # 首先隐藏父窗口
    root.withdraw()
    # 然后就是当前窗口的一些设置
    RFCcheck_window=Toplevel(root)
    RFCcheck_window.geometry('1005x592')
    RFCcheck_window.resizable(False, False)
    RFCcheck_window.attributes("-alpha", 0.9)
    RFCcheck_window.iconbitmap("img/scout.ico")

    # 剩下的事情就是在一个canvas画布上展开的了。
    photo = PhotoImage(file="img/9.png")
    # 画布
    canvas = Canvas(RFCcheck_window, width=1005, height=592)
    canvas.pack()
    # 背景
    canvas.create_image(0, 0, image=photo, anchor=NW)
    # 大标题
    canvas.create_text(500, 40, text="随机森林检测模块", font=('华文行楷', 40, 'bold'))

    # 选择检测路径按钮&选中检测路径后展示文本框
    select_check_button = Button(canvas,text="选择检测路径", font=('华文行楷', 20, 'bold'),command=lambda :RFCcheck_select_path(filelist_text))
    canvas.create_window(150, 120, window=select_check_button)
    select_entry = Entry(canvas,textvariable=filelist_text)
    canvas.create_window(20, 170, width=960, height=30, window=select_entry, anchor=W)

    # 选择模型路径按钮&选中模型路径后展示文本框
    select_model_button = Button(canvas,text="加载模型路径", font=('华文行楷', 20, 'bold'),command=lambda :RFCcheck_select_file(model_text))
    canvas.create_window(500, 120, window=select_model_button)
    model_entry = Entry(canvas,textvariable=model_text)
    canvas.create_window(20, 205, width=960, height=30, window=model_entry, anchor=W)
    # 获取路径结果
    print(filecheck_name)
    print(loadmodel_name)

    # 检测结果列表
    result_listbox = Listbox(canvas,listvariable=result)
    canvas.create_window(20, 420, width=960, height=300, window=result_listbox, anchor=W)
    # 检测按钮
    check_button = Button(canvas,text="开始检测", font=('华文行楷', 20, 'bold'),command=lambda :run_check(result_listbox))
    canvas.create_window(850, 120, window=check_button)
    # 检测结果标题
    canvas.create_text(500, 245, text="检测结果", font=('华文行楷', 30, 'bold'))

    # 添加关闭事件
    RFCcheck_window.protocol("WM_DELETE_WINDOW", lambda: close_second_window(RFCcheck_window))

# 一个重要的函数，关闭子窗口并且恢复父窗口
def close_second_window(second_window):
    # 销毁第二个窗口
    second_window.destroy()
    # 显示主窗口
    root.deiconify()

# 运行主窗口，控制各个模块的窗口的打开
def run_tkinter_root():
    # 一些root窗口的设置
    root.title("PHP-Webshell-Scout")
    root.geometry('1005x592')
    root.resizable(False, False)
    root.attributes("-alpha", 0.9)
    root.iconbitmap("img/scout.ico")
    photo = PhotoImage(file="img/9.png")

    # 画布
    canvas = Canvas(root, width=1005, height=592)
    # 背景
    canvas.create_image(0, 0, image=photo, anchor=NW)
    # 大标题
    canvas.create_text(500, 40, text="PHP-Webshell检测系统", font=('华文行楷', 40, 'bold'))

    # 四个功能模块按钮实现
    select_check_button = Button(canvas, text="随机森林训练模块", font=('华文行楷', 20, 'bold'),
                                 command=lambda: run_tkinter_RFCtrain())
    canvas.create_window(200, 150, window=select_check_button)
    select_check_button = Button(canvas, text="随机森林检测模块", font=('华文行楷', 20, 'bold'),
                                 command=lambda: run_tkinter_RFCcheck())
    canvas.create_window(800, 150, window=select_check_button)
    select_check_button = Button(canvas, text="神经网络训练模块", font=('华文行楷', 20, 'bold'),
                                 command=lambda: run_tkinter_NNtrain())
    canvas.create_window(200, 300, window=select_check_button)
    select_check_button = Button(canvas, text="神经网络检测模块", font=('华文行楷', 20, 'bold'),
                                 command=lambda: run_tkinter_NNcheck())
    canvas.create_window(800, 300, window=select_check_button)

    canvas.pack()

    root.mainloop()

if __name__ == "__main__":
    # 检测模块需要的全局变量
    filelist = {}
    pre_feature_value = []
    checked_filename = []

    # 训练模块需要的全局变量
    trainmodel = trainModel()
    dL = deepLearn()
    photo = None

    # 模型加载路径和需要进行检测的文件目录的默认值,PS：训练模型的一些路径需要到trainModel.py中修改
    loadmodel_name = r"traindata/rfc-default.pkl"
    filecheck_name = r"check"

    # 开启日志功能
    log()

    # 创建tkinter主窗口
    root = Tk()
    # 运行主窗口
    run_tkinter_root()

