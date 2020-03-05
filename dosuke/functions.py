from datetime import date
from pulp import *
import pandas as pd
import random

from .models import Band, Member

    
# 最大防音室利用可能コマ数
LEN_ALL_FRAME = 27

# 防音室使用可能枠
room_start = 0
room_end = 27
room_frames = [i for i in range(room_start, room_end)]

# セッション枠
session_start = 14
session_end = 20
session_frames = [i for i in range(session_start, session_end)]

def get_timetables(data):

    # とるコマの優先順
    frame_prim = [14,15,16,17,18,19,13,12,11,10,20,21,22,23,24,25,26,9,8,7,6,5,4,3,2,1,0]

    # 1日分のスケジュールを決定するごとに作る案の数
    N = 5

    # 結果用
    timetable_dict = {}

    for day in set(data['day']):
        
        timetables = []

        for n in range(N):
            hope_times = {}
            for band in set(data['band']):
                hope_times[band] = list(data[(data['band'] == band) & (data['day'] == day)]['hour'])

            # 練習枠の初期化
            timetable = [i for i in ['padding']*(LEN_ALL_FRAME+1)]
            # 防音室利用可能時間の箇所を None (空)にする
            for i in room_frames:
                timetable[i] = None

            # 優先順リストから、利用するコマのみ抽出
            frame_prim_tmp = frame_prim.copy()
            frame_prim_tmp = [i for i in frame_prim_tmp if i in room_frames]
                
            # セッション時間を確保
            if not any(timetable[session_start:session_end]):
                timetable[session_start:session_end] = ['session']*len(session_frames)
                frame_prim_tmp = [i for i in frame_prim_tmp if i not in session_frames]
            else:
                print('そのセッション希望時間は防音室が使えません')
            
            # バンド１周分時間帯をとってく
            for band in random.sample(hope_times.keys(), len(hope_times)):
                
                # 取ろうと思ってる時間長、3から
                hoped_len = 3

                # 他のバンド練の時間をずらす必要があるかどうか
                isTrouble = True
                
                # 各枠を開始時間とした時に入れることができるか順にみていく
                for start in frame_prim_tmp:
                    
                    # 前者: 取ろうとしてる枠が希望時間内に含まれてるか、後者: その時間が空いてるか
                    if set(hope_times[band]) >= set(range(start, start + hoped_len)) \
                            and not(any(timetable[start:start+hoped_len])):
                        timetable[start:start+hoped_len] = [band]*hoped_len
                        # とったら次のバンド
                        isTrouble = False
                        break

                # 取れなかったら他のバンド練をずらせるかを検討
                if isTrouble:
                    # ここでは希望条件を満たしてるかは最後に確かめる
                    for start in frame_prim_tmp:
                        
                        # 取ろうとしている枠が他のバンド練の間じゃないかチェック
                        if timetable[start-1] == timetable[start]:
                            continue
                        
                        # セッション前か後で詰める場所の捜索範囲を変更(例えば、セッション前に１枠、セッション後に1枠あっても詰められない)
                        # start がセッション前の場合、セッション前を調整範囲とする
                        if start < session_start:
                            adjust_start = room_start
                            adjust_end = session_start
                        # start がセッション後の場合、セッション後を調整範囲とする
                        elif start >= session_end:
                            adjust_start = session_end
                            adjust_end = room_end
                        else:
                            continue
                        adjust_table = timetable[adjust_start:adjust_end]
                        start_in_adjust = start - adjust_start

                        # start_in_adjust に近い値順に並べるための関数
                        sort_key_dist = lambda value : abs(value - start_in_adjust)

                        # None の数が足りなかったら
                        if adjust_table.count(None) < hoped_len:
                            # None を増やす(足りるまで繰り返す)
                            for q in range(hoped_len - adjust_table.count(None)):
                                # セッション以外で欲しい枠より多く枠を取得してるバンドを探して1枠をNoneにする
                                # start_in_adjust に近いとこからみてく# TODO 改善point 
                                for i in sorted([i for i in range(len(adjust_table)-hoped_len)], key=sort_key_dist):
                                    if len(set(adjust_table[i:i+hoped_len])) == 1 \
                                    and adjust_table[i] != 'session' \
                                    and adjust_table[i] != 'padding':
                                        adjust_table[i] = None
                                        break

                        # hoped_len分 None を start_in_adjust にもってくる（できるだけ start_in_adjust に近いやつ）
                        move_indexes = [i for i, x in enumerate(adjust_table) if x == None]
                        move_indexes.sort(key=sort_key_dist)
                        # Noneがhoped_len枠以上確保できてたら start_in_adjust に移動
                        if len(move_indexes) >= hoped_len:
                            
                            for i in range(hoped_len):
                                # インデックスの整合性を保つため、一時的に削除予定という値を代入
                                adjust_table[move_indexes[i]] = 'remove'
                            for i in range(hoped_len):
                                # start_in_adjust にバンド名を追加
                                adjust_table.insert(start_in_adjust, band)
                            adjust_table = [i for i in adjust_table if i != 'remove']

                            # 調整用に切り出した枠を全体に戻す、一旦tmpに置く
                            tmp_table = timetable.copy()
                            tmp_table[adjust_start:adjust_end] = adjust_table
                            
                            isError = False
                            # 希望時間とバッティングしないかチェック
                            # timetableに含まれてるバンドを対象
                            for b in set([b for b in tmp_table if b is not None and b != 'padding' and b != 'session']):
                                b_indexes = [i for i, x in enumerate(tmp_table) if x == b]
                                # もしずらしたことで希望時間から逸れた場合は適用しない
                                if not(all([i in hope_times[band] for i in b_indexes])):
                                    isError = True
                                    break
                            
                            # バッティングがなければ timetable に適用してこのバンドの枠確保は終了
                            if isError == False:
                                timetable = tmp_table.copy()
                                break

            # 最初と最後のバンドをできる限り3枠にする
            # padding と Noneを取り除いた timetable を valid_table とする
            valid_table = [i for i in timetable if (i is not None and i != 'padding')]
            
            # 最初のバンドが2枠だったら3枠に増やせるか試す
            if valid_table[0] != valid_table[2] and valid_table[0] != 'session':
                band = valid_table[0]
                b_index = timetable.index(band)
                
                # 他のバンドをずらせるか試す
                adjust_table = timetable[room_start:session_start]
                b_index_in_adjust = b_index - room_start
                # b_index_in_adjust に近い値順に並べるための関数
                sort_key_dist = lambda value : abs(value - b_index_in_adjust)
                
                # ずらすために None を確保
                # その後の時間に None がなければ3枠持ってるバンドを探してその一個を None にする
                if all(adjust_table[b_index_in_adjust:]):
                    for i in range(len(adjust_table)-2):
                        if adjust_table[i] == adjust_table[i+1] and adjust_table[i] == adjust_table[i+2]:
                            adjust_table[i] = None
                            break
                
                    # Noneが確保できてたら移動
                    move_indexes = [i for i, x in enumerate(adjust_table) if x == None]
                    move_indexes.sort(key=sort_key_dist)
                    
                    if len(move_indexes) > 0:
                        # 何個目の None を持ってくるか変えながらやって希望時間にバッティングしないものを探す
                        for i in move_indexes:
                            tmp_adjust_table = adjust_table.copy()
                            
                            # 削除挿入間でindexの変化が生じないように、一時的に削除予定という値を代入
                            tmp_adjust_table[i] = 'remove'
                            # 最初のバンドに枠を追加
                            tmp_adjust_table.insert(b_index_in_adjust, band)
                            tmp_adjust_table.remove('remove')

                            tmp_table = timetable.copy()
                            tmp_table[room_start:session_start] = tmp_adjust_table

                            isError = False
                            # 希望時間とバッティングしないかチェック
                            for b in set([i for i in tmp_table if i is not None and i != 'padding' and i != 'session']):
                                b_indexes = [i for i, x in enumerate(tmp_table) if x == b]
                                # もしずらしたことで希望時間から逸れた場合は適用しない
                                if not(all([i in hope_times[band] for i in b_indexes])):
                                #   if not(all([i in band_df.at[b, 'hoped_frames'] for i in b_indexes])):
                                    isError = True
                                    break

                            if isError == False:
                                timetable = tmp_table.copy()

            # 最初のバンドが2枠だったら3枠に増やせるか試す
            if valid_table[-3] != valid_table[-1] and valid_table[-1] != 'session':
                band = valid_table[-1]
                b_index = timetable.index(band)
                
                # 他のバンドをずらせるか試す
                adjust_table = timetable[session_end:room_end]
                b_index_in_adjust = b_index - session_end
                # b_index_in_adjust に近い値順に並べるための関数
                sort_key_dist = lambda value : abs(value - b_index_in_adjust)
        
                # ずらすために None を確保
                # その後の時間に None がなければ3枠持ってるバンドを探してその一個を None にする
                if all(adjust_table[:b_index_in_adjust]):
                    for i in range(len(adjust_table)-2):
                        if adjust_table[i] == adjust_table[i+1] and adjust_table[i] == adjust_table[i+2]:
                            adjust_table[i] = None
                            break

                    # Noneが確保できてたら移動
                    move_indexes = [i for i, x in enumerate(adjust_table) if x == None]
                    move_indexes.sort(key=sort_key_dist)
                    
                    if len(move_indexes) > 0:
                        # 何個目の None を持ってくるか変えながらやって希望時間にバッティングしないものを探す
                        for i in move_indexes:
                            tmp_adjust_table = adjust_table.copy()
                        
                            # 削除挿入間でindexの変化が生じないように、一時的に削除予定という値を代入
                            tmp_adjust_table[i] = 'remove'
                            # 最後のバンドに枠を追加
                            tmp_adjust_table.insert(b_index_in_adjust, band)
                            tmp_adjust_table.remove('remove')

                            tmp_table = timetable.copy()
                            tmp_table[session_end:room_end] = tmp_adjust_table

                            isError = False
                            # 希望時間とバッティングしないかチェック
                            for b in set([i for i in tmp_table if i is not None and i != 'padding' and i != 'session']):
                                b_indexes = [i for i, x in enumerate(tmp_table) if x == b]
                                # もしずらしたことで希望時間から逸れた場合は適用しない
                                #   if not(all([i in band_df.at[b, 'hoped_frames'] for i in b_indexes])):
                                if not(all([i in hope_times[b] for i in b_indexes])):
                                    isError = True
                                    break
                            if isError == False:
                                timetable = tmp_table.copy()

            timetables.append(timetable)
        
        # TODOスコア付けして timetables をソートする

        timetable_dict[day] = timetables[0]
                    
    return timetable_dict


def get_time_lavel():
  return [f'{(18+i)//2}:{(i%2)*3}0' for i in range(28)]


# 最適化問題を得方法
def get_timetables_with_pulp(data):

    data['name'] = data['band']
    for band_name in set(data['name']):
        band = Band.objects.get(name=band_name)
        data['band'][data['name'] == band_name] = band.pk

    timetable_dict = {}

    # 学年設定用に現在の年度を算出
    today = date.today()
    y = today.year
    m = today.month
    fy = y - (15-m)//12 # 年度

    band_list = []
    
    for band in Band.objects.all():
        grade_sum = 0
        for member in Member.objects.filter(band__name=band).all():
            grade_sum += fy - member.entry_year
        band_list.append([band.pk, grade_sum, band])

    bands = pd.DataFrame(band_list, columns=['band','grade_sum','name'])

    df = pd.DataFrame([
        (i
        ,j
        ,k
        ,j*l*0.1 if j<16 else (35-j)*l*0.1
        ,pulp.LpVariable(f'Var_{i}_{j}_{k}', cat=pulp.LpBinary)
        )
        for i in data['day'].unique()
        for j in data['hour'].unique()
        for k, l in zip(bands.band, bands.grade_sum)
    ], columns=['day', 'hour', 'band', 'rank', 'Var'])
    dff = df.drop(columns=['rank','Var'])

    #練習時間とリーダー学年×練習時間帯の最大化
    model = LpProblem(sense=LpMaximize)
    model +=  pulp.lpSum(df.Var) + pulp.lpDot(df.Var,df['rank'])

    #各時間に練習できるのは1バンドのみ
    for key, group in df.groupby(['day', 'hour']):
        model += pulp.lpSum(group.Var)<=1
    #1日に練習していいのは一回のみ
    for key, group in df.groupby(['day', 'band']):
        model += pulp.lpSum(group.Var)<=1
    #希望時間にそう様にする
    for key, group in df.groupby(['day', 'hour', 'band']):
        if len(data[(data.day==key[0])&(data.hour==key[1])&(data.band==key[2])]) == 0:
            model += lpSum(group.Var) == 0
        else:
            model += lpSum(group.Var) <= 1

    assert model.solve()

    df['Val'] = df.Var.apply(pulp.value)
    result = df[df.Val>0.5].drop(columns=['Var','Val'])

    # 練習枠の初期化
    timetable_base = [i for i in ['padding']*(LEN_ALL_FRAME+1)]

    # 防音室利用可能時間の箇所を None (空)にする
    for i in room_frames:
        timetable_base[i] = None

    for day in result['day']:
        timetable = timetable_base.copy()
        for hour in result[result['day'] == day]['hour']:
            band_pk = result[(result['day'] == day) & (result['hour'] == hour)]['band']
            timetable[hour] = Band.objects.get(id=band_pk)
        timetable_dict[day] = timetable

    return timetable_dict