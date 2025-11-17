import argparse
import getpass
import argon2
from typing import TypedDict, NotRequired

class HasherCustomParams(TypedDict):
    m: NotRequired[int]
    t: NotRequired[int]
    p: NotRequired[int]
    l: NotRequired[int]

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

def parse_customhasher_params(params_str: str) -> None:
    split_str = params_str.split(",")
    debug(f'Params_split:{split_str}')
    if (len(split_str) % 2) == 0:
        split_params = {split_str[i]: int(split_str[i + 1]) for i in range(0, len(split_str)-1, 2)}
        debug(f'Params:{split_params}')
        if check_params_valid(split_params):
            pass
        else:
            print('Will apply valid parameters, skipping undefined ones')
        
        params: HasherCustomParams = {'m': argon2.DEFAULT_MEMORY_COST,
                                        't': argon2.DEFAULT_TIME_COST,
                                        'p': argon2.DEFAULT_PARALLELISM,
                                        'l': argon2.DEFAULT_HASH_LENGTH}
        for key, value in split_params.items():
            params[key] = value
        debug(f'Final passed params:{params}')
        global ph
        ph = argon2.PasswordHasher(time_cost=params['t'], memory_cost=params['m'], parallelism=params['p'], hash_len=params['l'])
    else:
        print(f'Formatting Error, odd number of element passed in {params_str} for custom Hasher. Using default values.')

def check_params_valid(param_dict: dict[str,int]) -> bool:
    valid_param_keys = HasherCustomParams.__optional_keys__
    if all(key in valid_param_keys for key,_ in param_dict.items()):
        return True
    else:
        print('Invalid hasher parameter defined, please recheck input.')
        return False

def debug(message:str):
    if debug_flag:
        print(f'{message}')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-v','--verify', action='store_true', default= False, dest= "verify_flag", help= "Turn on verify mode to verify hash")
    argparser.add_argument('-d','--debug', action='store_true', default= False, dest= "debug_flag", help= "Turn on debug mode for printing debug messages")
    argparser.add_argument('-c','--customhasher', default= None, help= "Pass parameters to customise Hasher parameters as per argon2-cffi CLI interface. Separate options and values with `,` eg t,1,m,524288,p,4")
    argparser.add_argument('-ph','--pwdhash', help= "Enter hash to be verified with this flag")
    cmd_args = argparser.parse_args()

    debug_flag = cmd_args.debug_flag
    if cmd_args.customhasher is not None:
        parse_customhasher_params(cmd_args.customhasher)
    pwd_frm_usr = getpass.getpass("Password to hash/verify:")

    verify_flag = cmd_args.verify_flag
    if verify_flag:
        verify_hash(cmd_args.pwdhash, pwd_frm_usr)
    else:
        hash_pwd(pwd_frm_usr)