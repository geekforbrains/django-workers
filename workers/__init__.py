name = 'workers'


def task(*arg, **kwarg):
    from workers.worker import task
    return task(*arg, **kwarg)
