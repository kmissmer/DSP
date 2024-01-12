import os
import json
import datetime

def print_all_dicts(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        print(data)
                        print("\n\n")
                except json.JSONDecodeError as error:
                    print("Error parsing JSON:", str(error))




def find_things_in_comments(directory_path):
    files_with_names = 0
    files_with_email = 0
    files_with_citystate = 0
    files_with_phone = 0
    files_with_RD = 0
    attached_files = 0
    inline_files = 0
    earliest_date = None
    latest_date = None

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                try:
                    #parse into dict
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        #finds how many comments have names
                        if "firstName" in data['data']['attributes'] and data['data']['attributes']['firstName'] is not None \
                                and "lastName" in data['data']['attributes'] and data['data']['attributes']['lastName'] is not None:
                            files_with_names += 1

                        #finds how many comments have emails
                        if "email" in data['data']['attributes'] and data['data']['attributes']['email'] is not None:
                            files_with_email += 1

                        #finds how many comments have city/state
                        if "submitterRepCityState" in data['data']['attributes'] and data['data']['attributes']['submitterRepCityState'] is not None:
                            files_with_citystate += 1

                        #finds how many comments have phone numbers
                        if "phone" in data['data']['attributes'] and data['data']['attributes']['phone'] is not None:
                            files_with_phone += 1

                        #finds how many comments have a recieved date
                        if "receiveDate" in data['data']['attributes'] and data['data']['attributes']['receiveDate'] is not None:
                            files_with_RD += 1  
                        # finds how many comments have attached files vs inline files
                        if "comment" in data['data']['attributes'] and data ['data']['attributes']['comment'] is not None:
                            if "See attached file(s)" in data['data']['attributes']['comment']:
                                attached_files += 1
                            else:
                                inline_files += 1
                        # finds earliest and latest dates
                        receive_date_str = data['data']['attributes']['receiveDate']
                        if receive_date_str:
                            receive_date = datetime.datetime.fromisoformat(receive_date_str)
                            if earliest_date is None or receive_date < earliest_date:
                                earliest_date = receive_date
                            if latest_date is None or receive_date > latest_date:
                                latest_date = receive_date 

                except json.JSONDecodeError as error:
                    print("Error parsing JSON:", str(error))



    print(f"There are {files_with_names} names in the comments")
    print(f"There are {files_with_email} emails in the comments")
    print(f"There are {files_with_citystate} city/state in the comments")
    print(f"There are {files_with_phone} phone numbers in the comments")
    print(f"There are {files_with_RD} recieved dates in the comments")
    print(f"There are {attached_files} attached files in the comments")
    print(f"There are {inline_files} inline files in the comments")
    print(f"The earliest date is {earliest_date}")
    print(f"The latest date is {latest_date}")


def find_things_in_documents(directory_path):
    files_with_names = 0
    files_with_email = 0
    files_with_citystate = 0
    files_with_phone = 0
    files_with_RD = 0
    document_titles = []


    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                try:
                    #parse into dict
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                    #finds how many documents have names
                    if "firstName" in data['data']['attributes'] and data['data']['attributes']['firstName'] is not None \
                            and "lastName" in data['data']['attributes'] and data['data']['attributes']['lastName'] is not None:
                        files_with_names += 1
                    #finds how many documents have emails
                    if "email" in data['data']['attributes'] and data['data']['attributes']['email'] is not None:
                        files_with_email += 1
                    # finds how many documents have city/state
                    if "submitterRepCityState" in data['data']['attributes'] and data['data']['attributes']['submitterRepCityState'] is not None:
                        files_with_citystate += 1
                    # finds how many documents have phone numbers
                    if "phone" in data['data']['attributes'] and data['data']['attributes']['phone'] is not None:
                        files_with_phone += 1
                    #finds how many documents have a recieved date
                    if "receiveDate" in data['data']['attributes'] and data['data']['attributes']['receiveDate'] is not None:
                        files_with_RD += 1
                    if "title" in data['data']['attributes'] and data['data']['attributes']['title'] is not None:
                        document_titles.append(data['data']['attributes']['title'])


                except json.JSONDecodeError as error:
                    print("Error parsing JSON:", str(error))


    print(f"There are {files_with_names} names in the documents")
    print(f"There are {files_with_email} emails in the documents")
    print(f"There are {files_with_citystate} city/state in the documents")
    print(f"There are {files_with_phone} phone numbers in the documents")
    print(f"There are {files_with_RD} recieved dates in the documents")

    #for title in document_titles:
     #   print(title)
      #  print("\n")


if __name__ == "__main__":
    print_all_dicts("FDA/FDA-2012-N-1210/text-FDA-2012-N-1210")
    find_things_in_comments("FDA/FDA-2012-N-1210/text-FDA-2012-N-1210/comments")
    find_things_in_documents("FDA/FDA-2012-N-1210/text-FDA-2012-N-1210/documents")
