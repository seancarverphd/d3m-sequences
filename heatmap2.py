
import pandas as pd
import plotly.figure_factory as ff


def get_colors(path):

    with open(path) as small_df_csv:
        df = pd.read_csv(small_df_csv)
        columns = df.groupby('category').sum()
        columns = columns.sort_values('l2', ascending=False)
        categories = columns.index.tolist()

        rows = df.groupby('performer').sum()
        rows = rows.sort_values('l2', ascending=True)
        performers = rows.index.tolist()

        df = df.pivot_table(index=['performer'],
                            columns=['category'], values='l2').fillna(0)

        df2 = df.reindex(categories, axis=1)
        df3 = df2.reindex(performers, axis=0)

        data = df3.values.tolist()
    return categories, performers, data


def get_asterisk(path, categories, performers):

    with open(path) as sumdf_csv:
        new_df = pd.read_csv(sumdf_csv)
        new_df.best_string = new_df.best_string.fillna(' ')

        new_df = new_df.pivot_table(
            index=['performer'],
            columns=['category'],
            values=['best_string'],
            aggfunc=lambda x: ''.join(
                str(v) for v in x)).fillna("")
        new_df.columns = new_df.columns.get_level_values(1)

        df2 = new_df.reindex(performers, axis=0)
        df3 = df2.reindex(categories, axis=1)
        text = df3.values.tolist()
    return text


def create_heatmap(x_values, y_values, data, text):

    fig = ff.create_annotated_heatmap(
        z=data,
        x=x_values,
        y=y_values,
        annotation_text=text,
        showscale=True,
        colorbar=dict(
            title='l2 value'))
    fig.update_xaxes(side="bottom")
    fig.update_layout(
        xaxis=dict(
            title='Category'), yaxis=dict(
            title='Performer'))
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 5.5
    # fig.show()
    fig.write_image("heatmap2.pdf")


if __name__ == '__main__':
    x, y, data_values = get_colors('small_df.csv')
    z_text = get_asterisk('sumdf.csv', x, y)
    create_heatmap(x, y, data_values, z_text)
