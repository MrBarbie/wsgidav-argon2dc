import argparse
import getpass
import argon2
import timeit
from statistics import mean,stdev

ph = argon2.PasswordHasher()


def hash_pwd(password:str) -> None:
    hash_gen= ph.hash(password)
    print(hash_gen)

def verify_hash(hash:str, pwd:str) -> None:
    try:
        ph.verify(hash,pwd)
        print('\U00002705 Password matches hash')
    except argon2.exceptions.VerifyMismatchError:
        print('\U000026D4 Password does not match hash')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v','--verify', action='store_true', default= False, dest= "verify_flag", help= "Turn on verify mode to verify hash")
    argparser.add_argument('-t','--time', action='store_true', default= False, dest= "time_flag", help= "Turn on timing mode to check if parameters need to be tuned")
    argparser.add_argument('-ph','--pwdhash', help= "Enter hash to be verified with this flag")
    cmd_args = argparser.parse_args()
    pwd_frm_usr = getpass.getpass("Password to hash/verify:")
    verify_flag = cmd_args.verify_flag
    time_flag = cmd_args.time_flag
    if verify_flag:
        if time_flag:
            verify_time = timeit.repeat('verify_hash(cmd_args.pwdhash, pwd_frm_usr)', repeat=5, number=10, globals=globals())
            print(f'Avg_time: {mean(verify_time)} +- {stdev(verify_time)}\nList: {verify_time}')
        else:
            verify_hash(cmd_args.pwdhash, pwd_frm_usr)
    else:
        hash_pwd(pwd_frm_usr)