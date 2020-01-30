from PyInstaller.utils.cliutils.archive_viewer import do_cleanup, get_data, get_archive, stack


def get_my_content(arch, recursive, brief, output):
    if isinstance(arch.toc, dict):
        toc = arch.toc
        if brief:
            for name, info in toc.items():
                output.append(name)
        else:
            for key in toc:
                info = toc[key]
                toc[key] = [info, get_data(key, arch)]
            output.append([toc])
    else:
        toc = arch.toc.data
        for el in toc:
            if brief:
                output.append(el[5])
            else:
                output.append([el, get_data(el[5], arch)])
            if recursive:
                if el[4] in ('z', 'a'):
                    get_my_content(get_archive(
                        el[5]), recursive, brief, output)
                    stack.pop()


def get_all(filename):
    archive = get_archive(filename)
    stack.append((filename, archive))
    output = []
    get_my_content(archive, recursive=True, brief=False, output=output)
    do_cleanup()
    return output, archive
