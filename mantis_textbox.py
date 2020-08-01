def mantis_textbox(list_of_strings,
                   title='',
                   margin_char='*',
                   width=80,
                   vertical_margin_width=1,
                   horizontal_margin_width=1):
    import textwrap
    m_c = margin_char
    w = width
    v_m_w = vertical_margin_width
    h_m_w = horizontal_margin_width

    title_text = f'{title}'
    horizontal_margin_line = (w * m_c)[0:(w)]
    empty_line = f'{m_c * v_m_w}{" ":^{w - 2 * v_m_w * len(m_c)}}{m_c * v_m_w}'
    title_line = f'{m_c * v_m_w}{title_text:^{w - 2 * v_m_w * len(m_c)}}{m_c * v_m_w}'

    lines = [horizontal_margin_line for _ in range(h_m_w)]
    lines.append(empty_line)
    lines.append(title_line)
    lines.append(empty_line)

    for i, j in enumerate(list_of_strings):
        if (len(list_of_strings[i]) < (w - 2 * len(m_c) * v_m_w - 6)):

            meaning_line = f'''{m_c * v_m_w} {i + 1:02d}. {list_of_strings[i]:<{w - 2 * len(m_c) * v_m_w - 6}} {m_c * v_m_w}'''

            lines.append(meaning_line)
        else:
            wrapper = textwrap.TextWrapper(width=(w - 2 * len(m_c) * v_m_w -
                                                  6))
            splited_line = wrapper.wrap(text=(list_of_strings[i]))

            meaning_line = f'''{m_c * v_m_w} {i + 1:02d}. {splited_line[0]:<{w - 2 * len(m_c) * v_m_w - 6}} {m_c * v_m_w}'''

            lines.append(meaning_line)

            for i in range(1, len(splited_line)):

                intended_line = f'''{m_c * v_m_w}     {splited_line[i]:<{w - 2 * len(m_c) * v_m_w - 6}} {m_c * v_m_w}'''

                lines.append(intended_line)

    lines.append(empty_line)
    for _ in range(h_m_w):
        lines.append(horizontal_margin_line)

    textbox = '\n'.join(lines)

    return textbox
