
import pandas as pd
import plotly.figure_factory as ff


def get_colors(path):

    with open(path) as small_df_csv:
        df = pd.read_csv(small_df_csv)
        y_values = df.performer.unique().tolist()
        df = df.pivot_table(index=['performer'],
                            columns=['category'], values='l2').fillna(0)

        x_values = df.columns.values.tolist()
        data = df.values.tolist()
    return x_values, y_values, data


def get_asterisk(path):

    with open(path) as sumdf_csv:
        new_df = pd.read_csv(sumdf_csv)
        new_df.best_string = new_df.best_string.fillna(' ')

        new_df = new_df.pivot_table(
            index=['performer'],
            columns=['category'],
            values=['best_string'],
            aggfunc=lambda x: ''.join(
                str(v) for v in x)).fillna("")

        text = new_df.best_string.values.tolist()
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
            title='Performer'), title='')
    fig.update_coloraxes(dict(showscale=True))
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 5.5
    # fig.show()
    fig.write_image("heatmap.pdf")


if __name__ == '__main__':
    x, y, data_values = get_colors('small_df.csv')
    z_text = get_asterisk('sumdf.csv')
    create_heatmap(x, y, data_values, z_text)
