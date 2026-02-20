class Grouper:
    def __init__(self):
        pass

    def deduplicate_sequence(self, items: list):
        sequences = list()
        sequence_cur = list()
        for i, item in enumerate(items):
            if i == 0:
                sequence_cur.append(item)
                continue
            if item["description"] == sequence_cur[-1]["description"]:
                sequence_cur.append(item)
            else:
                sequences.append(sequence_cur)
                sequence_cur = [item]
        sequences.append(sequence_cur)

        sequences_dedup = list()
        for seq in sequences:
            if len(seq) == 0:
                continue
            first_item = seq[0]
            last_item = seq[-1]
            if first_item["time_start"] == last_item["time_start"]:
                sequences_dedup.append(first_item)
            else:
                item_inter = {**first_item}
                item_inter["time_start"] = first_item["time_start"]
                item_inter["time_duration"] = str((float(last_item["time_start"]) + float(last_item["time_duration"]))
                                                  - float(first_item["time_start"]))
                sequences_dedup.append(item_inter)
        return sequences_dedup