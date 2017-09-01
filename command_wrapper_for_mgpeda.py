
#add by me

    def infoh(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.infoh(victim)

    def getinfoh(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.getinfoh(victim)

    def ph(self):
        """ Print chunk information of victim"""
        #(arg,) = normalize_argv(arg,1)
        angelheap.ph()

    def getheaplist(self, *arg):
        """ Print chunk information of victim"""
        (lst,) = normalize_argv(arg,1)
        angelheap.getheaplist(lst)

    def ci(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.ci(victim)

    def cix(self,*arg):
        """ Print chunk information of victim"""
        (victim, ) = normalize_argv(arg,1)
        angelheap.cix(victim)

    def cixoff(self,*arg):
        """ Print chunk information of victim"""
        (victim, ) = normalize_argv(arg,1)
        angelheap.cixoff(victim)

    def allci(self):
        """ Print chunk information of victim"""
        angelheap.allci()

    def allcix(self):
        """ Print chunk information of victim"""
        angelheap.allcix()

#added by me

