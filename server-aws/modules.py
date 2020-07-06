import pandas as pd

pd.set_option("max_rows", 999)
import numpy as np


# ### 준비과정( DataFrame 불러오기)
class recipe_recomm:
    def __init__(self, user_musts, user_options):
        self.mapping_csv = pd.read_csv('ingredients_mapping.csv', encoding='cp949', header=None).rename(
            columns={0: 'original', 1: 'general'})
        self.df = pd.read_csv("tbRecipe_all.csv")
        self.df_vector = pd.read_csv("df_vector.csv", encoding='utf-8-sig', index_col='Unnamed: 0')
        self.total_ingredients = self.df_vector.columns[:].copy()
        self.my_dict = dict(zip(self.mapping_csv.original, self.mapping_csv.general))

        #########
        ## 빈 리스트 처리하기 - 둘 다 비어있을 때는 내가 정해둔 디폴트 값으로 처리
        if user_musts == [] and user_options == []:
            user_musts = ['김치', '마늘', '파']
            user_options = ['돼지고기', '계란', '파', '고추장', '간장', '떡', '닭고기']
        ########

        self.arr_musts = self.to_general_name(user_musts)
        self.arr_options = self.to_general_name(user_options)
        user_ingred = user_musts + user_options
        self.arr_ingreds = self.to_general_name(user_ingred)

    ###
    def to_general_name(self, lst):
        if lst == []:
            return np.array([])
        arr = np.array(lst)
        return np.vectorize(self.my_dict.get)(arr)

    ###

    # 입력받은 재료를 우리가 가진 이름으로 변환하기
    def filtering(self, df_vector, arr_musts):
        """df_vector(모든 레시피의 벡터데이터)에서
        사용자가 필수로 넣으려고 하는 재료가 없는 애들은 다 드랍시키기"""
        df_vector_test = df_vector.copy(deep=True)

        ##### 필수재료로 입력받은게 없을 경우 필터링 ㄴㄴ
        if len(arr_musts) == 0:
            return df_vector_test
        ######

        for must in arr_musts:
            df_vector_test = df_vector_test[lambda x: x[must] != 0]

        filter_indices = df_vector_test.index
        df_vector_test = df_vector.loc[filter_indices]
        return df_vector_test

    def my_vector(self, arr_ingreds):
        """ 총 재료에서 사용자가 입력한 모든 재료는 1로, 아닌것은 0으로"""
        my_vector = np.zeros(len(self.total_ingredients))
        ingredient_location_list = []
        not_in_list = []
        try:
            for ingredient in arr_ingreds:
                ingredient_location = np.where(np.array(self.total_ingredients) == ingredient)[0][0]
                ingredient_location_list.append(ingredient_location)
        except:
            pass
        my_vector[ingredient_location_list] = 1
        return my_vector

    def cosine_similarity(self, my_vector, new_df, df):
        """ 사용자 재료 벡터와 원래 벡터들의 유사도 구하기
        유사도 높은 애들을 조회수가 높은 순으로 sort하여 df형태로 반환,
        유사도 높은 애들의 재료 벡터 반환"""
        from scipy import spatial

        idx = new_df.index
        index_dictionary = {}

        for i in idx:
            x = np.array(new_df.loc[i])
            temp = 1 - spatial.distance.cosine(my_vector, x)
            index_dictionary[i] = temp

        df_vector_copy = new_df.reset_index()
        df_vector_copy['similarity'] = df_vector_copy['index'].map(index_dictionary)
        df_vector_copy = df_vector_copy.set_index('index')

        similar_recipe = df_vector_copy[df_vector_copy.similarity.isin(
            df_vector_copy[['similarity']].sort_values(by='similarity', ascending=False)['similarity'].head(12))]
        df_similar_recipe = df[df.id.isin(similar_recipe.index)].sort_values(by='조회수', ascending=False).head(8)
        df_similar_recipe = df_similar_recipe.reset_index(drop=True)

        similar_recipe_vector = df_vector_copy[df_vector_copy.index.isin(df_similar_recipe.id)]
        similar_recipe_vector = similar_recipe_vector.drop('similarity', axis=1)
        similar_recipe_vector.reset_index()

        return df_similar_recipe, similar_recipe_vector

    def extra_ingredients(self, df_similar_recipe, similar_recipe_vector, my_vector):
        """있는 재료 없는 재료 구분해서 따로 보여주기"""

        ingredient_list = np.array(similar_recipe_vector.columns)
        ingredient_check = similar_recipe_vector - my_vector  # 1이면 없는 재료, -1이면 안쓰는 재료

        necessary_dictionary = {}
        unused_dictionary = {}

        for index in ingredient_check.index:
            ingredient_check_per_recipe = np.array(ingredient_check.loc[index])

            necessary_ingredient_indices = np.where(ingredient_check_per_recipe == 1)[0]
            unused_ingredient_indices = np.where(ingredient_check_per_recipe == -1)[0]

            necessary_ingredient = list(ingredient_list[necessary_ingredient_indices])
            unused_ingredient = list(ingredient_list[unused_ingredient_indices])

            necessary_dictionary[index] = necessary_ingredient
            unused_dictionary[index] = unused_ingredient
        df_similar_recipe['더 필요한 재료'] = df_similar_recipe['id'].map(necessary_dictionary)
        df_similar_recipe['안 쓴 재료'] = df_similar_recipe['id'].map(unused_dictionary)

        return df_similar_recipe

    def to_json(self, similar_recipe):
        """ df 형태로 받은 similar recipe 정보를 json 형태로 바꾸기"""
        selected_recipe = {}
        for x in range(len(similar_recipe)):
            temp = similar_recipe.iloc[x, :]
            key = temp.id
            selected_recipe[int(key)] = {'title': temp[2], 'time': temp[5], 'image_url': temp[8],
                                         'recipe_url': temp[9], 'required_ingredients': temp[12],
                                         'unused_ingredients': temp[13]}
        return selected_recipe

    ### main ###
    def return_output(self):
        new_df = self.filtering(self.df_vector, self.arr_musts)
        my_Vector = self.my_vector(self.arr_ingreds)
        df_similar_recipe, similar_recipe_vector = self.cosine_similarity(my_Vector, new_df, self.df)

        output = self.to_json(self.extra_ingredients(df_similar_recipe, similar_recipe_vector, my_Vector))

        return output