#  -*- coding:utf-8 -*-


def merge_data(member_info, coupon_info):
    member_size = member_info.shape[0]
    coupon_size = coupon_info.shape[0]
    
    member_info = member_info.apply(
        lambda x: pd.concat([x for i in range(coupon_size)], axis=0)
    ).sort_index().reset_index(drop=True)

    coupon_info = pd.concat([coupon_info for i in range(member_size)], axis=0).reset_index(drop=True)
    
    return pd.concat([coupon_info, member_info], axis=1)
