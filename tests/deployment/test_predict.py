import great_expectations as ge
import predict
import pytest


@pytest.fixture
def video():
    video = {
        "index": 12,
        "channelId": "UCeXY-D7RTVIIOuKP9HB35Ig",
        "videoCategoryId": 10,
        "channelViewCount": 25000,
        "videoCount": 20,
        "subscriberCount": 200,
        "videoId": "--NZRkXBV7k",
        "channelelapsedtime": 80000,
        "channelCommentCount": 8,
        "videoViewCount": 10000,
        "elapsedtime": 22000,
        "videoDislikeCount": 1,
        "videoPublished": "2015-03-30T04:04:40.000Z",
        "VideoCommentCount": 2,
    }
    return video


def test_prepare_data(video):
    df = predict.prepare_data(video)
    df = ge.dataset.PandasDataset(df)

    selected_columns = [
        "index",
        "channelId",
        "videoCategoryId",
        "channelViewCount",
        "videoCount",
        "subscriberCount",
        "videoId",
        "channelelapsedtime",
        "channelCommentCount",
        "videoViewCount",
        "elapsedtime",
        "videoDislikeCount",
        "videoPublished",
        "VideoCommentCount",
    ]

    df.expect_table_columns_to_match_ordered_list(
        column_list=selected_columns
    )  # schema adherence

    df.expect_column_values_to_be_between(
        column="videoViewCount", min_value=0, strict_min=True
    )  # positive values
    df.expect_column_values_to_be_between(
        column="videoDislikeCount", min_value=0, strict_min=True
    )  # positive values
    df.expect_column_values_to_be_between(
        column="VideoCommentCount", min_value=0, strict_min=True
    )  # positive values

    df.expect_column_values_to_be_of_type(
        column="channelId", type_="category"
    )  # type adherence
    df.expect_column_values_to_be_of_type(column="videoId", type_="category")
    df.expect_column_values_to_be_of_type(column="videoPublished", type_="category")


def test_predict(video):
    data = predict.prepare_data(video)
    prediction = predict.predict(data)
    assert prediction == 42
