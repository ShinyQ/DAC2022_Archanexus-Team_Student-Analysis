import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_df():
    df = pd.read_csv('./static/Data_kualifikasi.csv', sep=';')
    return df


def get_box_plot_data(labels, bp):
    rows_list = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i*2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i*2)+1].get_ydata()[1]
        rows_list.append(dict1)

    return pd.DataFrame(rows_list)


def space():
    st.write("\n")
    st.write("\n")


def sankey_dataset(df):
    columns = [
        'Tinggal_Dengan', 'Status_Kerja',
        'Biaya', 'Tgl_Daftar_Kuliah', 'Alamat',
        'UKM', 'Organisasi_Kampus', 'Fakultas', 'Lama_Kuliah'
    ]

    col1, _ = st.columns([3, 1])

    with col1:
        options = st.multiselect(
            'Pilih Urutan Kolom',
            columns,
            columns
        )

    df["Biaya"] = df.Biaya.map(
        {"Beasiswa": "Beasiswa", "Orang Tua": "Ortu", "Kosong": "Tidak Diisi"})
    df["UKM"] = df.UKM.map({"UKM_1": "UKM 1", "UKM_2": "UKM 2",
                           "UKM_3": "UKM 3", "UKM_4": "UKM 4", "Tidak": "Tidak Ada"})
    df["Organisasi_Kampus"] = df.Organisasi_Kampus.map(
        {"Ya": "Ya", "Tidak": "Tidak Ikut"})

    if len(options) > 0:
        temp = []

        for i in range(0, len(options)):
            if i == 0:
                df_temp1 = df.groupby(["Gender", options[i]])[
                    "Nama"].count().reset_index()
                df_temp1.columns = ["source", "target", "value"]
            else:
                df_temp1 = df.groupby(
                    [options[i-1], options[i]])["Nama"].count().reset_index()
                df_temp1.columns = ["source", "target", "value"]

            temp.append(df_temp1)

        links = pd.concat(temp, axis=0)
        unique_source_target = list(
            pd.unique(links[["source", "target"]].values.ravel("K")))
        mapping_dict = {k: v for v, k in enumerate(unique_source_target)}

        links["source"] = links["source"].map(mapping_dict)
        links["target"] = links["target"].map(mapping_dict)
        links_dict = links.to_dict(orient="list")

        fig = go.Figure(data=[go.Sankey(
            valueformat=".0f",
            node=dict(
                pad=15,
                thickness=15,
                label=unique_source_target
            ),

            link=dict(
                source=links_dict["source"],
                target=links_dict["target"],
                value=links_dict["value"]
            )
        )])

        fig.update_layout(
            font_size=16,
            height=400,
            width=1100,
            margin_pad=0,
            margin=dict(l=0, r=0, t=20, b=20),
        )

        st.plotly_chart(fig)


def pie_ukm_fakultas(df):
    df = df.loc[:, ["UKM", "Fakultas"]]

    col1, col2 = st.columns([3, 9])

    with col1:
        choose_columns = st.selectbox(
            'Silahkan Pilih Kolom', df["UKM"].unique())

    space()
    col1, col2, _ = st.columns([5, 4, 1])

    with col1:
        df_faculty = df.loc[lambda df: df['UKM'] == choose_columns]
        df_faculty = dict(df_faculty['Fakultas'].value_counts())
        df_faculty = df_faculty.items()
        df_faculty = pd.DataFrame(list(df_faculty), columns=[
                                  "Fakultas", "Jumlah"])

        fig = px.pie(df_faculty, values='Jumlah', names='Fakultas')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            font_size=16,
            height=300,
            width=450,
            margin=dict(l=0, r=0, t=0, b=0),
            margin_pad=0
        )

        st.plotly_chart(fig)

    with col2:
        st.markdown(f'##### Deskripsi Jumlah Fakultas Pada {choose_columns}:')
        st.table(df_faculty)


def pie_alamat_fakultas(df):
    df = df.loc[:, ["Alamat", "Fakultas"]]

    col1, col2 = st.columns([3, 9])

    with col1:
        choose_columns = st.selectbox(
            'Silahkan Pilih Kolom', df["Fakultas"].unique())

    space()
    col1, col2, _ = st.columns([5, 4, 1])

    with col1:
        df_faculty = df.loc[lambda df: df['Fakultas'] == choose_columns]
        df_faculty = dict(df_faculty['Alamat'].value_counts())
        df_faculty = df_faculty.items()
        df_faculty = pd.DataFrame(
            list(df_faculty), columns=["Alamat", "Jumlah"])

        fig = px.pie(df_faculty, values='Jumlah', names='Alamat')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            font_size=16,
            height=300,
            width=450,
            margin=dict(l=0, r=0, t=0, b=0),
            margin_pad=0
        )

        st.plotly_chart(fig)

    with col2:
        st.markdown(
            f'##### Deskripsi Jumlah Alamat Pada Fakultas {choose_columns}:')
        st.table(df_faculty)


def barplot_year_description(df):
    col1, col2, _ = st.columns([9, 4, 2])

    columns = list(df.columns)
    columns.remove('Nama')
    columns.remove('Tgl_Daftar_Kuliah')

    with col1:
        options = st.multiselect('Pilih Urutan Kolom', columns, columns)

    with col2:
        choose_columns = st.selectbox('Pilih Tahun Dataset', df["Tgl_Daftar_Kuliah"].unique())

    df_temp = df.loc[lambda df: df['Tgl_Daftar_Kuliah'] == choose_columns]
    df_temp = df_temp.loc[:, options]

    items = []

    for i, column in enumerate(options):
        df_selected = dict(df_temp[column].value_counts())
        items.append([i, list(df_selected.keys()), list(df_selected.values())])

    fig = go.Figure()

    for i, data in enumerate(items):
        arr_key = data[0]

        for i in range(len(data[1])):
            temp_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            temp_arr[arr_key] = data[2][i]

            fig.add_trace(go.Bar(
                y=options,
                x=temp_arr,
                name=data[1][i],
                orientation='h',
                text=data[1][i] +
                " (" + str(round(data[2][i] / len(df_temp), 2)) + "%) ",
                hoverinfo="x",
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=16,
                    font_family="Rockwell"
                )
            ))

    fig.update_layout(
        barmode='stack',
        font_size=16,
        height=450,
        width=1050,
        extendpiecolors=True,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=False,
        hoverlabel_align='left',
    )

    st.plotly_chart(fig)


def funnel_three_and_a_half_year(df):

    col1, col2, col3, _ = st.columns([3, 3, 3, 3])

    with col1:
        choose_tinggal = st.selectbox('Silahkan Pilih Tinggal Dengan', df["Tinggal_Dengan"].unique())
        space()
    
    with col2:
        choose_status = st.selectbox('Silahkan Pilih Status Kerja', df["Status_Kerja"].unique())
    
    with col3:
        choose_biaya = st.selectbox('Silahkan Pilih Biaya', df["Biaya"].unique())
    
    df_funnel = pd.DataFrame(columns=["Kolom", "Jumlah"])

    df_funnel = df_funnel.append({
        "Kolom": f'Tinggal Dengan: {choose_tinggal}',
        "Jumlah": df["Tinggal_Dengan"].value_counts()[choose_tinggal]
    }, ignore_index=True)

    count = len(df.query(f'Tinggal_Dengan == "{choose_tinggal}" and Status_Kerja == "{choose_status}"'))
    
    df_funnel = df_funnel.append({
        "Kolom": f'Status kerja: {choose_status}', 
        "Jumlah": count
    }, ignore_index=True)

    count = len(df.query(f'Tinggal_Dengan == "{choose_tinggal}" and Status_Kerja == "{choose_status}" and Biaya == "{choose_biaya}"'))
    
    df_funnel = df_funnel.append({
        "Kolom": f'Dibiayai oleh: {choose_biaya}', 
        "Jumlah": count
    }, ignore_index=True)

    count = len(df.query(f'Tinggal_Dengan == "{choose_tinggal}" and Status_Kerja == "{choose_status}" and Biaya == "{choose_biaya}" and Lama_Kuliah == "3,5"'))
    
    df_funnel = df_funnel.append({
        "Kolom": '3.5 Tahun', 
        "Jumlah": count
    }, ignore_index=True)

    col1, col2, _ = st.columns([5, 4, 1])
   
    with col1:
        fig = go.Figure(go.Funnel(
            y=df_funnel["Kolom"],
            x=df_funnel["Jumlah"],
            textposition="inside",
            textinfo="value+percent initial",
             marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal", "silver"],
                    },
            )
        )

        fig.update_layout(
            font_size=15,
            height=300,
            width=600,
            margin=dict(l=0, r=0, t=0, b=0),
            margin_pad=0
        )

        st.plotly_chart(fig)

    with col2:
        st.table(df_funnel)


def boxplot_year(df_pure):

    df = df_pure.copy()
    df["Lama_Kuliah"] = df["Lama_Kuliah"].str.replace(',', '.')
    df['Lama_Kuliah'] = df['Lama_Kuliah'].astype(float)

    columns = [
        'Tinggal_Dengan', 'Status_Kerja',
        'Biaya', 'UKM', 'Organisasi_Kampus', 'Fakultas'
    ]
    
    col1, _ = st.columns([3, 9])
    
    with col1:
        choose_column = st.selectbox('Silahkan Pilih Kolom', columns)

    fig = px.box(
        df, x=choose_column, y="Lama_Kuliah", 
        color=choose_column,
        labels={
            "Lama_Kuliah": "Lama Kuliah",
            f'{choose_column}': choose_column.replace('_', ' ')
        }
    )

    st.plotly_chart(fig)

    fig = px.box(
        df_pure, x=columns, y="Lama_Kuliah",
        notched=True,
        labels={
            "Lama_Kuliah": "Lama Kuliah",
            "value": "Jenis Kolom"
        }
    )
    
    fig.update_layout(
        font_size=14,
        height=450,
        width=1100,
        margin=dict(l=0, r=0, t=0, b=0),
        margin_pad=0
    )

    st.plotly_chart(fig)    


def app():
    st.markdown("# Halaman Analisis Dataset")
    st.write("Pada halaman ini ditampilkan analisis terkait data mahasiswa yang ada.")
    df = get_df()

    st.markdown("#### Bagaimana Persentase Fakultas Berdasarkan UKM Yang Diikuti?")
    st.markdown("""Pie chart di bawah ini menampilkan persebaran fakultas anggota dari masing-masing ukm. 
                Hasil menunjukkan bahwa semua fakultas tersebar rata pada tiap-tiap UKM.""")

    pie_ukm_fakultas(df)

    space()


    st.markdown("#### Bagaimana Persentase Kota Tinggal Berdasarkan Fakultas?")
    st.markdown("""Pie chart di bawah ini menampilkan persebaran kota tinggal anggota dari tiap-tiap fakultas. 
                Hasil menunjukkan bahwa persebaran kota tinggal mahasiswa tersebar rata pada setiap fakultas.""")

    pie_alamat_fakultas(df)

    space()

    st.markdown("#### Bagaimana Persebaran Data Setiap Kolom Berdasarkan Tahun?")
    st.markdown("""Diagram batang dibawah menunjukkan persebaran data pada dataset untuk tiap tahun pendaftaran 
                mahasiswa pada Universitas XYZ. Terdapat tiga tahun pendaftaran yang ada pada dataset ini yaitu 
                2007, 2008, dan 2009. User dapat memilih untuk menampilkan atribut tertentu dengan mengatur Urutan
                Kolom. Ketika diagram batang di-hover, akan memunculkan jumlah dari data tersebut.""")

    barplot_year_description(df)

    space()

    st.markdown("#### Sankey Diagram")
    st.markdown("""Sankey diagram dibawah ini mendeskripsikan alir atau laju dari berbagai atribut pada dataset ini. 
                Pada diagram ini terdapat informasi incoming dan outcoming flow serta jumlah dari suatu “source” menuju “target” 
                dari tiap-tiap entitas yang terdapat pada setiap atribut pada dataset. User dapat memilih untuk menampilkan 
                attribut tertentu dengan mengatur Urutan Kolom.""")
    
    sankey_dataset(df)

    space()

    st.markdown("#### Apa Saja Pengaruh Mahasiswa Dapat Lulus 3.5 Tahun ?")
    st.markdown("""Funnel chart di bawah ini akan menampilkan berapa persentase dan jumlah mahasiswa yang lulus 3.5 
                tahun dari kategori yang ditentukan oleh user. Terdapat tiga kategori yang dapat diubah oleh user, yaitu mahasiswa 
                tersebut tinggal dengan siapa, status kerja mahasiswa, dan sumber biaya perkuliahan mahasiswa.""")

    funnel_three_and_a_half_year(df)

    space()

    st.markdown("#### Boxplot Lama Kuliah")
    st.markdown("""Box plot ini dapat dipilih oleh user dari berbagai atribut yang ada pada dataset terhadap Lama Kuliah 
                mahasiswa. Dari box plot ini, diharapkan user dapat mengetahui bagaimana pengaruh atribut lain seperti status kerja 
                mahasiswa terhadap lama kuliahnya.""")
    
    boxplot_year(df)
