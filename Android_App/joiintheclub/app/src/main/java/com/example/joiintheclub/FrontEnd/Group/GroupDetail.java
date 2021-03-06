package com.example.joiintheclub.FrontEnd.Group;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.view.View;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;

import com.example.joiintheclub.FrontEnd.Init.LoginActivity;
import com.example.joiintheclub.FrontEnd.Setting.SettingMain;
import com.example.joiintheclub.FrontEnd.UserProfile.UserProfileMain;
import com.example.joiintheclub.R;

import java.util.Arrays;
import java.util.List;

@SuppressLint("Registered")
public class GroupDetail extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
    RecyclerView.Adapter adapter;
    Button group_detail_back_btn;
    Button announcement_btn;
    Button poll_btn;
    Button event_btn;
    Button inbox_btn;
    ImageButton groupProfileBtn;
    Dialog mDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_group_detail);

        recyclerView = findViewById(R.id.group_detail_recycle_view);
        layoutManager = new LinearLayoutManager(this);
        recyclerView.setLayoutManager(layoutManager);
        recyclerView.setHasFixedSize(true);



      //  String[][] pollInfo = Group.GetPolls("15");
        String[][] pollInfo;
        pollInfo = new String[1][5];

            pollInfo[0][1] = "Favorite Color ?";
            pollInfo[0][2] = "question";
            pollInfo[0][3] = "poll_response_options";
            pollInfo[0][4] = "poll_description";


        String [] PollNameBuf = new String[pollInfo.length];

        for(int a = 0; a < pollInfo.length; a++)
        {

            PollNameBuf[a]= pollInfo[a][1];

        }
        List<String> pollName = Arrays.asList(PollNameBuf);


       // String[][] AnnInfo = Group.GetAnnouncements("15");
        String[][] AnnInfo;
        AnnInfo = new String[1][5];
        AnnInfo[0][0]  = "leader_id";
        AnnInfo[0][1] = "Meeting on Sunday";
        AnnInfo[0][2] = "poll_response_options";
        AnnInfo[0][3] = "poll_description";


        String [] AnnNameBuf = new String[AnnInfo.length];
        String sd;


        for(int a = 0; a < pollInfo.length; a++)
        {

            AnnNameBuf[a]= AnnInfo[a][1];
        }

        List<String> AnnName = Arrays.asList(AnnNameBuf);



        adapter = new GroupDetailRecycleAdapter(pollName,AnnName);
        recyclerView.setAdapter(adapter);


         group_detail_back_btn = findViewById(R.id.group_detail_back_btn);
         announcement_btn = findViewById(R.id.announcement_btn);
         poll_btn = findViewById(R.id.poll_btn);
         event_btn = findViewById(R.id.event_btn);
         inbox_btn = findViewById(R.id.inbox_btn);
         groupProfileBtn = findViewById(R.id.group_profile_pic);
         mDialog = new Dialog(this);


         group_detail_back_btn.setOnClickListener(new View.OnClickListener() {
             @Override
             public void onClick(View v) {
                 finish();
             }
         });

        announcement_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openAnnouncementDialog();
            }
        });

        poll_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openVoteDialog();

            }
        });

        event_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openEventDialog();
            }
        });

        inbox_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openInboxDialog();
            }
        });

        groupProfileBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });


        Toolbar toolbar = (Toolbar) findViewById(R.id.GDbar);
        setSupportActionBar(toolbar);


        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.group_detail_drawer);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.groupDetailNav);
        navigationView.setNavigationItemSelectedListener(this);
    }

    private void openAnnouncementDialog() {

        final AutoCompleteTextView title;
        final AutoCompleteTextView announcement_content;
        ImageButton close_btn;
        ImageView announce;


        mDialog.setContentView(R.layout.activity_announcement);
        mDialog.show();

        title = mDialog.findViewById(R.id.Ititle);
        announcement_content = mDialog.findViewById(R.id.Icontent);
        close_btn = mDialog.findViewById(R.id.Inbox_close_icon);
        announce = mDialog.findViewById(R.id.Inbox_publish);

        close_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDialog.dismiss();
            }
        });

        announce.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String stitle = title.getText().toString();
                String Content = announcement_content.getText().toString();
                String n;
            }
        });

    }

    private void openVoteDialog() {

        final AutoCompleteTextView title;
        final AutoCompleteTextView vote_content;
        ImageButton close_btn;
        ImageView vote;


        mDialog.setContentView(R.layout.activity_vote);
        mDialog.show();

        title = mDialog.findViewById(R.id.Vtitle);
        vote_content = mDialog.findViewById(R.id.Vcontent);
        close_btn = mDialog.findViewById(R.id.vote_close_icon);
        vote = mDialog.findViewById(R.id.Inbox_publish);

        close_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDialog.dismiss();
            }
        });

        vote.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String stitle = title.getText().toString();
                String Content = vote_content.getText().toString();
                String n;
            }
        });

    }

    private void openEventDialog() {

        final AutoCompleteTextView title;
        final AutoCompleteTextView event_content;
        ImageButton close_btn;
        ImageView event;


        mDialog.setContentView(R.layout.activity_event);
        mDialog.show();

        title = mDialog.findViewById(R.id.Ititle);
        event_content = mDialog.findViewById(R.id.Icontent);
        close_btn = mDialog.findViewById(R.id.Inbox_close_icon);
        event = mDialog.findViewById(R.id.Inbox_publish);

        close_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDialog.dismiss();
            }
        });

        event.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String stitle = title.getText().toString();
                String Content = event_content.getText().toString();
                String n;
            }
        });

    }

    private void openInboxDialog() {

        final AutoCompleteTextView title;
        final AutoCompleteTextView inbox_content;
        ImageButton close_btn;
        ImageView inbox;


        mDialog.setContentView(R.layout.activity_inbox);
        mDialog.show();

        title = mDialog.findViewById(R.id.Ititle);
        inbox_content = mDialog.findViewById(R.id.Icontent);
        close_btn = mDialog.findViewById(R.id.Inbox_close_icon);
        inbox = mDialog.findViewById(R.id.Inbox_publish);

        close_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mDialog.dismiss();
            }
        });

        inbox.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String stitle = title.getText().toString();
                String Content = inbox_content.getText().toString();
                String n;
            }
        });

    }


    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.group_detail_drawer);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }




    //@SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(@NonNull MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.profile) {
            Intent intent = new Intent(GroupDetail.this, UserProfileMain.class);
            startActivity(intent);
        } else if (id == R.id.search) {
            Intent intent = new Intent(GroupDetail.this, com.example.joiintheclub.FrontEnd.SearchGroup.SearchMain.class);
            startActivity(intent);

        } else if (id == R.id.club) {
            Intent intent = new Intent(GroupDetail.this, GroupMain.class);
            startActivity(intent);

        } else if (id == R.id.setting) {
            Intent intent = new Intent(GroupDetail.this, SettingMain.class);
            startActivity(intent);

        } else if (id == R.id.logout) {
            Intent intent = new Intent(GroupDetail.this, LoginActivity.class);
            startActivity(intent);
        }

        DrawerLayout drawer = findViewById(R.id.group_detail_drawer);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
