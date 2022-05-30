define s = Character("Sylvie", image="sylvie", color="#c88fc8")

screen space_invaders:
    default game = SpaceInvaders()

    add game


label start:

    s "Play space invaders"
    call screen space_invaders

    $ is_win, stats = _return
    $ score = stats["score"]
    $ time = stats["time"]
    $ wave = stats["wave"]

    if is_win:
        s "Nice you won. You destroyed all of them in [time] seconds."
    else:
        s "You destroyed [score] ships. Made it to wave [wave]. You survived [time] seconds"
    return

    