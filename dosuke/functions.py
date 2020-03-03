def getTimetables(hope_times):
  import pandas as pd
  import random
  from datetime import date

  # 学年設定用に現在の年度を算出
  today = date.today()
  y = today.year
  m = today.month
  fy = y - (15-m)//12 # 年度

  # バンドメンバー
  band_member_dict = {'NAGATA': ['NAGATA', 'KAUCHI', 'ISHIWATA', 'SAKAI', 'WATANABE', 'TAKIZAWA'],
                      'OGURI': ['OGURI', 'OHYA', 'JITSUKAWA', 'TAKIZAWA'],
                      'HASHIMOTO': ['HASHIMOTO', 'WATANABE', 'UMEZU'],
                      'ITO': ['ITO', 'TANAKA', 'UMEZU'],
                      'SUDO': ['SUDO', 'KAGEYAMA', 'MORI', 'KANEKO', 'KURIHARA', 'NUMAMOTO'],
                      'NUMAMOTO': ['IKEMIYA', 'JINNAI', 'SHIKAUCHI', 'NAGATA', 'TANAKA', 'NUMAMOTO'],
                      'SUGIMOTO': ['IKEMIYA', 'ISHIMORI', 'SUGIMOTO', 'JITSUKAWA'],
                      'ISHIDA': ['ISHIDAtp', 'KAUCHI', 'KATO', 'KANEKO', 'ISHIDAb', 'SUDO'],
                      'OKA': ['JINNAI', 'MARUYAMA', 'HANZAWA', 'WATANABE', 'OKA'],
                      'KAWAKAMI': ['MAEKAWA', 'HIRATA', 'KAWAKAMI', 'KAMIYAMA', 'NUMAMOTO'],
                      'MAEKAWA': ['MAEKAWA', 'IIDA', 'KOSAKA', 'IGUMA', 'SUDO'],
                      'OKITA': ['HIRATA', 'SUDO', 'OKITA', 'JITSUKAWA', 'SAIGA']
                    }

  # メンバー
  members_set = set()
  for band_member_array in band_member_dict.values():
      members_set |= set(band_member_array)
      
  # 学年とメンバー
  member_df = pd.DataFrame([['HANZAWA', 2016],
                            ['HASHIMOTO', 2016],
                            ['HIRATA', 2018],
                            ['IGUMA', 2019 ],
                            ['IIDA', 2019],
                            ['IKEMIYA', 2018],
                            ['ISHIDAb', 2015],
                            ['ISHIDAtp', 2019],
                            ['ISHIMORI', 2017],
                            ['ISHIWATA', 2015],
                            ['ITO', 2017],
                            ['JINNAI', 2019],
                            ['JITSUKAWA', 2018],
                            ['KAGEYAMA', 2019],
                            ['KAMIYAMA', 2019],
                            ['KANEKO', 2018],
                            ['KATO', 2019],
                            ['KAUCHI', 2019],
                            ['KAWAKAMI', 2019],
                            ['KOSAKA', 2019],
                            ['KURIHARA', 2017],
                            ['MAEKAWA', 2019],
                            ['MARUYAMA', 2017],
                            ['MORI', 2019],
                            ['NAGATA', 2016],
                            ['NUMAMOTO', 2018],
                            ['OGURI', 2019],
                            ['OHYA', 2019],
                            ['OKA', 2014],
                            ['OKITA', 2018],
                            ['SAIGA', 2018],
                            ['SAKAI', 2014],
                            ['SHIKAUCHI', 2018],
                            ['SUDO', 2017],
                            ['SUGIMOTO', 2018],
                            ['TAKIZAWA', 2015],
                            ['TANAKA', 2017],
                            ['UMEZU', 2015],
                            ['WATANABE', 2016],
                          ],
                          columns=['name', 'entry_year'])

  member_df.set_index('name', inplace=True)

  # 学年計算
  member_df['grade_val'] = fy - member_df['entry_year']
  grades = ['C', 'D', 'E', 'F', 'G', 'A', 'H', 'HiC']
  grade_list = []
  for index in range(len(member_df)):
      grade_list.append(grades[fy - member_df.iloc[index]['entry_year']])
  member_df['grade'] = grade_list

  # 時間枠リストの作成
  # 30分で１枠
  # time_frames[0]: '9:00~9:30'
  # time_frames[1]: '9:30~10:00'
  # ...
  # time_frames[26]: '22:00~22:30'
  time_frames = [f'{(18+i)//2}:{(i%2)*3}0~{(18+i+1)//2}:{((i+1)%2)*3}0' for i in range(27)]

  # 防音室使用可能枠
  room_start = 0
  room_end = 27
  room_frames = [i for i in range(room_start, room_end)]

  # セッション開始終了時刻
  session_start = 14
  session_end = 20
  session_frames = [i for i in range(session_start, session_end)]

  # # 練習枠のコマ数
  # practice_lens = [2,3]

  # とるコマの優先順
  frame_prim = [14,15,16,17,18,19,13,12,11,10,20,21,22,23,24,25,26,9,8,7,6,5,4,3,2,1,0]


  # 希望時間の入力
  # 今回は適当に決める
  # 連続している枠ごとにリストを作って2重リストとする
  hoped_frames_dict = {'NAGATA': [[i for i in range(0, 27)]],
                    'OGURI': [[i for i in range(0, 10)], [22,23, 24, 25]],
                    'HASHIMOTO': [[i for i in range(0,27)]],
                    'ITO': [[i for i in range(5,16)]],
                    'SUDO': [[i for i in range(0,4)]],
                    'NUMAMOTO': [[i for i in range(20,27)]],
                    'SUGIMOTO': [[i for i in range(0,0)]],
                    'ISHIDA': [[i for i in range(0,27)]],
                    'OKA': [[i for i in range(0,27)]],
                    'KAWAKAMI': [[i for i in range(0,27)]],
                    'MAEKAWA': [[i for i in range(8,10)]],
                    'OKITA': [[i for i in range(0,0)]],
                    }

  # band ごとの希望状況に関するデータフレームを作成
  band_df = pd.DataFrame(index=list(hoped_frames_dict.keys()), columns=['hoped_frames_lists', 'hoped_frames', 'hoped_frame_len_max'])
  # band_df = pd.DataFrame(index=list(hoped_time_dict.keys()), columns=['name', 'hoped_frames', 'hoped_time_len', 'booked_range'])

  for band_name, hope_frames in hoped_frames_dict.items():
      band_df.at[band_name, 'hoped_frames_lists'] = hoped_frames_dict[band_name]
      # 二重リストから一重リストに変換
      band_df.at[band_name, 'hoped_frames'] = [frame for frames in hoped_frames_dict[band_name] for frame in frames]
      # 長くて何時間使いたいか（多くても1時間分しか希望しないバンドがある場合などに使用）
      band_df.at[band_name, 'hoped_frame_len_max'] = max([len(frames) for frames in hoped_frames_dict[band_name]])
      

  N = 5
  timetables = []

  # 案を複数出す
  for n in range(N):
      
      frame_prim_tmp = frame_prim.copy()
      # 練習枠の初期化
      timetable = [i for i in ['padding']*(len(time_frames)+1)]
      for i in room_frames: 
          timetable[i] = None
      frame_prim_tmp = [i for i in frame_prim_tmp if i in room_frames]
          
      # セッション時間を確保
      timetable[session_start:session_end] = ['session']*len(session_frames)
      frame_prim_tmp = [i for i in frame_prim_tmp if i not in session_frames]
      
      # バンド１周分時間帯をとってく
      for band in random.sample(band_member_dict.keys(), len(band_member_dict)):
          
          # 取ろうと思ってる時間長
          hoped_len = 3
          # 元々1時間分しか希望してないバンドは取ろうとしてる枠数を2にする
          if band_df.at[band, 'hoped_frame_len_max'] == 2:
              hoped_len = 2
          # １時間以上希望してない場合はスキップ（TODO: 30分しか希望しないバンドも許容）
          elif band_df.at[band, 'hoped_frame_len_max'] < 2:
              continue

          # 他のバンド練の時間をずらす必要があるかどうか
          isTrouble = True
          
          # 各枠を開始時間とした時に入れることができるか順にみていく
          for start in frame_prim_tmp:
              
              # 取ろうとしてる枠が希望時間内に含まれてるか
              isHope = True
              for i in range(hoped_len):
                  if start + i not in band_df.at[band, 'hoped_frames']:
                      isHope = False
                      break
                  
              # 取れるか判定
              if isHope and not(any(timetable[start:start+hoped_len])):
                  timetable[start:start+hoped_len] = [band]*hoped_len
                  # とったら次のバンド
                  isTrouble = False
                  break

          # 取れなかったら次のバンド練をずらせるかを検討
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

                  # 3枠取ろうとしててNoneが3枠分なかったら2枠にする
                  if len([i for i in adjust_table if i is None]) < hoped_len:
                      hoped_len = 2

                      # None を2枠に増やす(2枠以上になるまで繰り返す)
                      for q in range(hoped_len - len([i for i in adjust_table if i is None])):
                          # セッション以外で3枠取得してるバンドを探して1枠をNoneにする
                          # start_in_adjust に近いとこからみてく
                          for i in sorted([i for i in range(len(adjust_table)-2)], key=sort_key_dist):
                              if adjust_table[i] == adjust_table[i+1] \
                              and adjust_table[i] == adjust_table[i+2] \
                              and adjust_table[i] != 'session' \
                              and adjust_table[i] != 'padding':
                                  adjust_table[i] = None
                                  break

                  # hoped_len分 None を start_in_adjust にもってくる（できるだけ start_in_adjust に近いやつ）
                  move_indexes = [i for i, x in enumerate(adjust_table) if x == None]
                  move_indexes.sort(key=sort_key_dist)
                  # Noneが2枠以上確保できてたら start_in_adjust に移動
                  if len(move_indexes) >= 2:
                      
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
                          if not(all([i in band_df.at[b, 'hoped_frames'] for i in b_indexes])):
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
                          if not(all([i in band_df.at[b, 'hoped_frames'] for i in b_indexes])):
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
                          if not(all([i in band_df.at[b, 'hoped_frames'] for i in b_indexes])):
                              isError = True
                              break
                      if isError == False:
                          timetable = tmp_table.copy()

      timetables.append(timetable)
                  
  return timetables

def getTimeLavel():
  return [f'{(18+i)//2}:{(i%2)*3}0' for i in range(28)]