import Model
# input_seq = ["ik","aag","sī","vo","bhī","ab","ke","saath","thī"]
# generated_seq=Model.generate_sequence((input_seq))
# print("Generated Sequence:", ' '.join(generated_seq))
def array_to_string(word_list):
    return ' '.join(word_list)
def text_to_array(text):
    return text.split()
global shayri
global generated_seq
def user_input(User_Data,No_of_Lines):
    k=False
    global shayri
    global generated_seq
    for i in range(No_of_Lines):
        if k == False:
            input_seq=text_to_array(User_Data)
            generated_seq=Model.generate_sequence((input_seq))
            shayri = array_to_string(generated_seq)
            k=True
        else:
            generated_seq=Model.generate_sequence((generated_seq))
            New_shayri=array_to_string(generated_seq)
            shayri=shayri+"\n"+New_shayri
    return shayri


# User_data=input("Please Input The Data :: ")
# num = int(input("Please Enter The Number of lines you want to genrate: "))
# getdata=user_input(User_data,num)
# print(getdata)