#Import Library
import matplotlib.pyplot as plt
#Buka File
with open("chatkelas12sph.txt") as file:
    lines = file.read().split("\n") 
    
    #jam teramai
    date_perhour = []
    
    #orang paling aktif
    data_username = []

    #topik yang sering dibicarakan
    data_topic = []

    #jam daring juan
    data_daring = []

    #Potong dan input data kedalam list sesuai dengan apa yang diperlukan
    for line in lines:
        #Waktu
        Time= line.split(":")[0].split(",")
        date_perhour.append(Time)

        #orang
        user = line.split('-')[1].split(':')[0]
        data_username.append(user)

        #TOpik
        topic = line.split('-')[1].split(':')[1].split()
        for one_topics in topic: #penggunaan for berguna untuk mengilangkan bentuk list didalam list 
            data_topic.append(one_topics)

        #daring
        daring = line.split()[:4]
        data_daring.append (daring)
    
    
    
    # #mengitung jumlah chat di jam tersebut    
    def count_hour_to_dict (input):
        new_dictionary= {}
        for time_index in range (24):
            new_dictionary[time_index] = 0 #membuat nol dari jam 1-jam 24
        for count_time in input:
            new_dictionary[count_time] += 1
        return new_dictionary

    #fungsi untuk menghitung 
    def count_to_dict (input):
        new_dictionary= {}
        for data in input:
            if data in new_dictionary:
                new_dictionary[data] += 1
            else:
                new_dictionary[data] = 1
        return new_dictionary
    
    #memisahkan dictionary ke list
    def count_to_list(input):
        new_list1 = []
        new_list2 = []
        for listing in input:
            new_list1.append(input[listing]) #value
            new_list2.append(listing) #key
        return new_list1,new_list2
    
    #fungsi Sorting dari besar ke kecil
    def sorting_by_its_value (key,value):
        for check in range(len(value)):
            for order in range(len(value)-1):
                if value[order] < value[order+1]:
                    temp = value[order]
                    value[order] = value[order+1]
                    value[order+1] = temp
                    temp2 = key[order]
                    key[order] = key[order+1]
                    key[order+1] = temp2
                else:
                    pass
        return key,value
    
    #Mencari kata yang ingin dicari
    def find_picked_topic (key,value,findword):
        for word in range(len(key)):
            if key[word] == findword:
                the_key = key[word]
                the_value = value[word]
        return the_key,the_value

#1. mencari 3 kombinasi hari jam yang paling sibuk
    #memisahkan jam dari tiap tanggal kedalam dictionary
    hour_date = {}
    date_list = []
    for date in date_perhour:
        if date[0] in hour_date: #jika data tanggal sudah ada di dict
            hour_date[date[0]].append(int(date[1])) #masukan kumpulan data jam yang ada menjadi value 
        else:
            hour_date[date[0]] = [int(date[1])] #memasukan key date[0] dan value date[1] kedalam dictionary
            date_list.append(date[0]) 
   
    #mencari hari palig sibuk
    most_busy_day= {}
    for find in hour_date:
        most_busy_day[find] = int(len(hour_date[find])) 
    chats,dating = count_to_list(most_busy_day) 
    most_chats_day, frequency_of_chat = sorting_by_its_value(dating,chats) 

    Timelist_date1 = hour_date[most_chats_day[0]] #menyimpan data jam kedalam variabel
    Timelist_date2 = hour_date[most_chats_day[1]] 
    Timelist_date3 = hour_date[most_chats_day[2]]
    
    # Jam sibuk dalam dict
    data_jam_day1 = count_hour_to_dict(Timelist_date1)
    data_jam_day2 = count_hour_to_dict(Timelist_date2)
    data_jam_day3 = count_hour_to_dict(Timelist_date3)
    
    # Jam sibuk dan frequency
    chat_frequency_day1,hour_name1 = count_to_list(data_jam_day1) 
    chat_frequency_day2,hour_name1 = count_to_list(data_jam_day2)
    chat_frequency_day3,hour_name1 = count_to_list(data_jam_day3)

#2 mencari top 3 orang terberisik
    #menghitung kedalam dic
    count_user = count_to_dict(data_username)
    #memisahkan dic ke dalam list
    userchat_frequency,user_name = count_to_list (count_user)
    #mengurutkan berdasarkan value
    sorted_username, sorted_chat_frequency = sorting_by_its_value (user_name, userchat_frequency)
    
#3. Top 5 Topic yang sering dibahas
    #menghitung kedalam dic
    count_topic = count_to_dict (data_topic)
    #memisahkan dic ke list
    total_chats,topic = count_to_list (count_topic)
    #mengurutkan berdasarkan value
    sorted_topic, sorted_total_chats = sorting_by_its_value (topic, total_chats)
    

    picked_topic = ["lampung","makan","binus","sekolah","maen"] 
    #mendapatkan Value dari kata yang dicari
    found_topic = []
    total_picked_frequency = []
    for find_topic in picked_topic:
        founded_key,founded_value = find_picked_topic(sorted_topic,sorted_total_chats,find_topic)
        found_topic.append (founded_key)
        total_picked_frequency.append (founded_value)
        #['lampung', 'makan', 'binus', 'sekolah', 'maen'][7, 5, 5, 4, 4]


#4. mencari jam daring juan       
    #memisahkan Jam dan tanggal untuk juan
    tanggal_daring_juan = []
    for index in data_daring:
        if index[3]== "Juan:": #cari yang namanya juan
            tanggal_daring_juan.append(index[0])
        else:
            pass
    
    #Jam Daring Juan
    jumlah_chat_perday = count_to_dict(tanggal_daring_juan)
    jumlah_daring,tanggal_daring = count_to_list(jumlah_chat_perday)

    
    # waktu_daring,tanggal_daring
    # #mencari jam 
    # integer_waktu_daring =[]
    


    
    # MEmbuat Data yang ada menjadi Grafik
    canvas_ = plt.figure()
    fig1 = canvas_.add_subplot(3,2,1)
    fig1.plot (hour_name1,chat_frequency_day1, label = 'Day 1')
    fig1.plot (hour_name1,chat_frequency_day2, label = 'Day 2')
    fig1.plot (hour_name1,chat_frequency_day3, label = 'Day 3')
    plt.xlabel ("Jam")
    plt.ylabel ("Chats Frequency")
    plt.legend ()
    plt.title ("Data Jam Sibuk Dalam 3 Hari")
    fig2 = canvas_.add_subplot (3,2,2)
    fig2.bar (sorted_username[:3], sorted_chat_frequency[:3])
    plt.xlabel ("Nama")
    plt.ylabel ("Chats Frequency")
    plt.title ("3 Orang Paling Aktif")
    fig3 = canvas_.add_subplot (3,2,5)
    fig3.bar (picked_topic,total_picked_frequency)
    plt.xlabel ("Topic")
    plt.ylabel ("Chat Frequency")
    plt.title ("5 Topik yang Sering Dibahas")
    fig4 = canvas_.add_subplot(3,2,6)
    fig4.bar (date_list,jumlah_daring)
    plt.xlabel ("Tanggal")
    plt.ylabel ("Jumlah Chat")
    plt.title ("Data Daring Juan")
    plt.show()