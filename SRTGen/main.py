from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import moviepy.editor as mp
import datetime
import speech_recognition as sr
import subprocess
from textblob import TextBlob


def root_config():
    root.iconbitmap("icon.ico")
    root.title("SRT Generator (English + Hindi) with Sentiment Analysis")
    root.config(bg=defaultbg)
    root.geometry("760x625")


def logo_fun():
    logo = Image.open("logo.png")
    logo_trace_img = ImageTk.PhotoImage(logo)
    img_label = Label(image=logo_trace_img)
    img_label.image = logo_trace_img
    img_label.grid(column=1, row=0)


def example_fun():
    example = Image.open("example.png")
    example_trace_img = ImageTk.PhotoImage(example)
    example_label = Label(image=example_trace_img)
    example_label.image = example_trace_img
    example_label.grid(column=1, row=10)


def print_line_fun(a):
    for i in range(3):
        Label(root, text="<><><><><><><><><><><>",
              bg=defaultbg).grid(column=i, row=a)


def print_space_line_fun(a):
    for i in range(3):
        Label(root, text=" ", bg=defaultbg).grid(column=i, row=a)


def unedit_label_fun():
    logo_fun()
    example_fun()
    print_space_line_fun(1)
    print_line_fun(2)
    print_space_line_fun(3)
    print_space_line_fun(5)
    print_line_fun(6)
    print_space_line_fun(7)
    print_space_line_fun(9)
    print_space_line_fun(11)
    print_line_fun(12)
    print_space_line_fun(13)
    print_space_line_fun(15)
    print_line_fun(16)
    print_space_line_fun(17)
    print_space_line_fun(19)
    print_line_fun(20)
    path_label = Label(root, text="Select Path To File : ",
                       font=("Helvetica", 12), bg=defaultbg)
    path_label.grid(column=0, row=8)
    example_label = Label(root, text="Example Path : ",
                          font=("Helvetica", 12), bg=defaultbg)
    example_label.grid(column=0, row=10)
    status_label = Label(root, text="Status : ",
                         font=("Helvetica", 12), bg=defaultbg)
    status_label.grid(column=0, row=18)


def the_status_bar():
    sta = Label(root, text="Idle", bd=1, relief="sunken",
                font=("Helvetica", 10), bg=defaultbg)
    sta.grid(column=1, row=18)
    return sta


def task_to_perform_fun():
    tasks = \
        [
            "0 -- Select Some Task --",
            "1 -- Generate English SRT only. --",
            "2 -- Generate SRT Along with Sentiment Analysis",
            "3 -- Generate Hindi SRT from English Video"
        ]
    task_var = StringVar(root)
    task_var.set(tasks[0])
    choice = OptionMenu(root, task_var, *tasks)
    choice.config(bg=defaultbg)
    choice.grid(column=1, row=4)
    return task_var


def browse(a):
    a.delete(0, tkinter.END)
    filename = tkinter.filedialog.askopenfilename()
    a.insert('end', filename)


def browse_and_enter_path():
    path_entry = Entry(root, bd=1, width=60, bg=defaultbg)
    path_entry.grid(column=1, row=8)
    browsebutton = Button(root, text="Browse", bg=defaultbg,
                          command=lambda: browse(path_entry))
    browsebutton.grid(column=2, row=8)
    return path_entry


def perform_gen(action_to_perform, ref_path):
    temp_path = ref_path.get()
    if temp_path == "":
        tkinter.messagebox.showinfo("OOPS!", "You forgot to choose a path?!")
    else:
        if temp_path[-3:] == "mp4":
            path_srt = path_convert(temp_path, "srt")
            path_wav = path_convert(temp_path, "wav")
            genwav(temp_path, path_wav)
            gensub(action_to_perform, path_srt, temp_path, path_wav)
        elif temp_path[-3:] == "wav":
            path_srt = path_convert(temp_path, "srt")
            gensub(action_to_perform, path_srt, temp_path, temp_path)
        else:
            tkinter.messagebox.showinfo(
                "Wait!", "Currently, This Software, Only Works Over mp4 And wav Files\nOr You Are Trying To Input Wrong File.")


def path_convert(t_path, f_mat):
    temp_list = t_path.split('.')
    temp_list[-1] = f_mat
    return ('.'.join(temp_list))


def genwav(t_path, p_wav):
    mp4_file_path = mp.VideoFileClip(t_path)
    mp4_file_path.audio.write_audiofile(p_wav)
    mp4_file_path.reader.close()


def gensub(a_t_p, p_srt, p_temp, p_wav):
    ref = mp.VideoFileClip(p_temp)
    dur = int(ref.duration) + 1
    ref.reader.close()
    iterable = int(dur/5) + 1
    start_time = datetime.datetime(2019, 1, 1, 00, 00, 00)
    end_time = end = start_time + datetime.timedelta(0, 5)
    if a_t_p == 1:
        gen_eng_sub(p_srt, p_wav, start_time, end_time, iterable)
    elif a_t_p == 2:
        gen_eng_sent_sub(p_srt, p_wav, start_time, end_time, iterable)
    elif a_t_p == 3:
        gen_hin_sub(p_srt, p_wav, start_time, end_time, iterable)
    else:
        tkinter.messagebox.showinfo(
            "Bad Error", "Some Unexplained Error Has Occur")


def wav_del(path_wav):
    wav_del_query = tkinter.messagebox.askquestion(
        "WAV Delete?", "Do You Want To Delete Corresponding WAV?")
    if wav_del_query == 'yes':
        del_path = ['del']
        del_path.insert(1, path_wav)
        del_path[1] = del_path[1].split('/')
        del_path[1] = '\\'.join(del_path[1])
        subprocess.call(del_path, shell=True)
        tkinter.messagebox.showinfo("Success", "Wav File Removed.")
        status.config(text="SRT Generation Successful.")
        tkinter.messagebox.showinfo(
            "Project By...", "Tenam Sobti.")
    else:
        status.config(text="SRT Generation Successful.")
        tkinter.messagebox.showinfo(
            "Project By...", "CS - 4th Year - B\nTEnam Sobti\nSObin Simon\nShivam Keshari")


def perform(re_toperform, re_path):
    performable = int(re_toperform.get()[0])
    if performable == 0:
        tkinter.messagebox.showinfo(
            "Task?", "Please select appropriate Action.")
    elif performable == 1 or performable == 2 or performable == 3:
        perform_gen(performable, re_path)
    else:
        tkinter.messagebox.showerror(
            "Bad Error", "Some unrecognised error has occur!")


def perform_task(r_toperform, r_path):
    perform_action = Button(root, text="Perform Specified Action",
                            bg=defaultbg, command=lambda: perform(r_toperform, r_path))
    perform_action.grid(column=1, row=14)


def check_sentiment(t_s_p):
    if t_s_p == 0:
        return "Neutral"
    elif t_s_p > 0 and t_s_p <= 0.25:
        return "Relaxed"
    elif t_s_p > 0.25 and t_s_p <= 0.5:
        return "Happy"
    elif t_s_p > 0.5 and t_s_p <= 0.75:
        return "Very Happy"
    elif t_s_p > 0.75 and t_s_p <= 1:
        return "Motivated"
    elif t_s_p < 0 and t_s_p >= (-0.25):
        return "Tensed"
    elif t_s_p < (-0.25) and t_s_p >= (-0.5):
        return "Sad"
    elif t_s_p < (-0.5) and t_s_p >= (-0.75):
        return "Very Sad"
    elif t_s_p < (-0.75) and t_s_p >= (-1):
        return "Depressed"


def gen_eng_sub(p_srt, p_wav, st, et, it):
    r = sr.Recognizer()
    sample = sr.AudioFile(p_wav)
    with sample as source:
        for i in range(it):
            audio = r.record(source, duration=5)
            try:
                text = r.recognize_google(audio, language='us-EN')
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
                text = "----------"
            to_be_written = "{0}\n{1} --> {2}\n{3}\n\n".format(
                i + 1, str(st.time()), str(et.time()), text)
            if i == 0:
                file = open(p_srt, "w")
            else:
                file = open(p_srt, "a")
            file.write(to_be_written)
            file.close()
            st = et
            et = st + datetime.timedelta(0, 5)
    tkinter.messagebox.showinfo(
        "Success!", "An English SRT is Successfully Generated!")
    wav_del(p_wav)


def gen_eng_sent_sub(p_srt, p_wav, st, et, it):
    net_polarity = 0
    net_iter = 0
    r = sr.Recognizer()
    sample = sr.AudioFile(p_wav)
    with sample as source:
        for i in range(it):
            audio = r.record(source, duration=5)
            try:
                text = r.recognize_google(audio, language='us-EN')
                text_blob_text = TextBlob(text)
                text_sentiment_polarity = text_blob_text.sentiment.polarity
                sentiment = check_sentiment(text_sentiment_polarity)
                net_polarity = net_polarity + text_sentiment_polarity
                net_iter = net_iter + 1
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
                text = "----------"
                sentiment = "None"
            to_be_written = "{0}\n{1} --> {2}\n[Sentiment : {3}]\n{4}\n\n".format(
                i + 1, str(st.time()), str(et.time()), sentiment, text)
            if i == 0:
                file = open(p_srt, "w")
            else:
                file = open(p_srt, "a")
            file.write(to_be_written)
            file.close()
            st = et
            et = st + datetime.timedelta(0, 5)
    net_sentiment = check_sentiment(net_polarity/net_iter)
    tkinter.messagebox.showinfo(
        "Success!", "An English SRT Along With Sentiment is Generated!")
    tkinter.messagebox.showinfo(
        "Net Sentiment", "The Net Sentiment of The Video Was : " + net_sentiment)
    wav_del(p_wav)


def gen_hin_sub(p_srt, p_wav, st, et, it):
    r = sr.Recognizer()
    sample = sr.AudioFile(p_wav)
    with sample as source:
        for i in range(it):
            audio = r.record(source, duration=5)
            try:
                text = r.recognize_google(audio, language='us-EN')
                text_blog_text = TextBlob(text)
                translated_hin_text = str(
                    text_blog_text.translate(from_lang='en', to='hi'))
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
                text = "----------"
                translated_hin_text = "----------"
            to_be_written = "{0}\n{1} --> {2}\n{3}\n\n".format(
                i + 1, str(st.time()), str(et.time()), translated_hin_text)
            if i == 0:
                file = open(p_srt, "w", encoding="utf-8")
            else:
                file = open(p_srt, "a", encoding="utf-8")
            file.write(to_be_written)
            file.close()
            st = et
            et = st + datetime.timedelta(0, 5)
    tkinter.messagebox.showinfo(
        "Success!", "Hindi SRT is Successfully Generated!")
    wav_del(p_wav)


defaultbg = "white"
root = Tk()
root_config()
unedit_label_fun()
status = the_status_bar()
toperform = task_to_perform_fun()
path = browse_and_enter_path()
perform_task(toperform, path)

root.mainloop()
